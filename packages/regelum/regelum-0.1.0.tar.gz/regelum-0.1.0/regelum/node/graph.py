"""Graph node implementation module.

This module provides the Graph class that manages collections of nodes and their execution.
Graphs handle:
- Node dependency resolution and execution ordering
- Hierarchical composition of nodes
- Time synchronization and step size management
- Reset behavior coordination (through ResetOnStep and ZeroOrderHold modifiers)
- Parallel execution preparation
- Logging and debugging support

Key concepts:
- Graphs are themselves nodes, enabling hierarchical composition
- They manage execution order based on dependencies
- They coordinate time steps across continuous and discrete nodes
- They support parallel execution through subgraph detection
"""

from __future__ import annotations
from typing import (
    Dict,
    List,
    Optional,
    Set,
    Any,
    Tuple,
    TYPE_CHECKING,
    Sequence,
)
from copy import deepcopy
from functools import reduce
from math import gcd

from regelum.node.base import Node
from regelum.node.core.inputs import Inputs, ResolvedInputs
from regelum.node.interfaces.base import IVariable
from regelum.node.interfaces.graph import IGraph
from regelum.node.interfaces.base import IInputs
from regelum.node.logging import Clock, StepCounter, Logger
from regelum.node.reset import Reset
from regelum.node.modifiers.reset import ResetOnStep
from regelum.node.modifiers.zero_order_hold import ZeroOrderHold
from regelum.node.core.types import ResolveStatus
from regelum.utils.logger import logger
from regelum.utils import find_scc

if TYPE_CHECKING:
    from regelum.node.parallel import ParallelGraph


class Graph(Node, IGraph[Node]):
    """A container and manager for interconnected nodes.

    Graphs serve multiple crucial roles:
    1. Dependency Management:
       - Resolve node dependencies
       - Determine correct execution order
       - Validate input/output connections

    2. Execution Control:
       - Coordinate time steps
       - Handle continuous/discrete node interactions
       - Support parallel execution

    3. State Management:
       - Coordinate resets across nodes
       - Handle logging and debugging
       - Support Monte Carlo simulations

    Attributes:
        _nodes: List of managed nodes
        _clock: Optional clock for time synchronization
        debug: Whether to enable detailed logging
        n_step_repeats: Number of times to repeat step execution
        resolve_status: Current dependency resolution status

    Example:
        ```python
        # Create nodes
        pendulum = Pendulum()
        controller = PDController(kp=10, kd=2)
        reset = ResetEachNSteps("pendulum_1", n_steps=100)

        # Create graph with time management
        graph = Graph(
            [pendulum, controller, reset],
            initialize_inner_time=True,
            debug=True,
            states_to_log=["pendulum_1.state"]
        )

        # Resolve dependencies and run
        graph.resolve(graph.variables)
        for _ in range(1000):
            graph.step()
        ```
    """

    _nodes: List[Node]
    _clock: Optional[Clock]
    debug: bool
    n_step_repeats: int
    resolve_status: ResolveStatus

    def __init__(
        self,
        nodes: List[Node],
        debug: bool = False,
        n_step_repeats: int = 1,
        initialize_inner_time: bool = False,
        states_to_log: Optional[List[str]] = None,
        logger_cooldown: float = 0.0,
        name: str = "graph",
    ) -> None:
        """Initialize Graph node.

        This constructor handles several crucial setup tasks:
        1. Time Management:
           - Computes fundamental step size from node step sizes
           - Sets up clock if inner time tracking is requested
           - Aligns discrete nodes with continuous time steps

        2. Reset Handling:
           - Processes reset nodes and applies modifiers
           - Sets up reset coordination between nodes

        3. Logging Setup:
           - Configures state logging if requested
           - Sets up logging cooldown to manage data collection

        Args:
            nodes: List of nodes to manage
            debug: Enable detailed logging and visualization
            n_step_repeats: Number of times to repeat step execution
            initialize_inner_time: Whether to track time internally
            states_to_log: List of variable names to log
            logger_cooldown: Minimum time between log entries
            name: Base name for the graph node

        Example:
            ```python
            # Basic graph with time management
            graph = Graph([node1, node2], initialize_inner_time=True)

            # Graph with logging
            graph = Graph(
                [node1, node2],
                states_to_log=["node1.state", "node2.output"],
                logger_cooldown=0.1 # (real-world time in seconds between consecutive log entries)
            )
            ```
        """
        super().__init__(name=name)
        fundamental_step_size = self._validate_and_set_step_sizes(nodes)
        self.step_size = fundamental_step_size
        if initialize_inner_time:
            self._clock = Clock(fundamental_step_size)
            step_counter = StepCounter([self._clock], start_count=0)
            nodes.append(step_counter)
            nodes.append(self._clock)
            self._align_discrete_nodes_execution_with_step_size(
                [
                    discrete_node
                    for discrete_node in nodes
                    if not discrete_node.is_continuous
                    and not isinstance(discrete_node, Clock)
                ]
            )
        self._process_resets(nodes)
        if states_to_log:
            self._setup_logger(
                nodes, states_to_log, logger_cooldown, fundamental_step_size
            )
        self._nodes = nodes
        self.debug = debug
        self.n_step_repeats = n_step_repeats
        self._collect_node_data()
        self.resolve_status = ResolveStatus.UNDEFINED

    @property
    def nodes(self) -> List[Node]:
        """Get list of nodes in the graph."""
        return self._nodes

    @nodes.setter
    def nodes(self, nodes: List[Node]) -> None:
        """Set list of nodes in the graph."""
        self._nodes = nodes

    def _process_resets(self, nodes: List[Node]) -> None:
        """Process reset nodes and apply modifiers."""
        reset_semaphores = [node for node in nodes if isinstance(node, Reset)]
        for reset_semaphore in reset_semaphores:
            corresponding_node = next(
                (
                    node
                    for node in nodes
                    if node.external_name
                    == "_".join(reset_semaphore.name.split("_")[1:])
                ),
                None,
            )
            if corresponding_node:
                self.apply_reset_modifier(corresponding_node, reset_semaphore)

    def apply_reset_modifier(self, node: Node, reset_semaphore: Node) -> None:
        """Apply reset modifier to a node."""
        RESET_INSTANCE_INDEX = -1
        RECIPIENT_NAME_START_INDEX = 1
        reset_semaphore_recipient = "_".join(
            reset_semaphore._internal_name.split("_")[
                RECIPIENT_NAME_START_INDEX:RESET_INSTANCE_INDEX
            ]
        )
        assert (
            reset_semaphore_recipient == node._internal_name
        ), f"Reset semaphore recipient and node internal name do not match: {reset_semaphore_recipient} != {node._internal_name}"
        ResetOnStep(node, reset_semaphore).bind_to_node(node)

    def _align_discrete_nodes_execution_with_step_size(
        self, discrete_nodes: List[Node]
    ) -> None:
        """Align discrete nodes with the fundamental step size."""
        if not hasattr(self, "clock"):
            raise ValueError("Clock not found in graph")

        for node in discrete_nodes:
            if isinstance(node, Graph):
                for subnode in node.nodes:
                    ZeroOrderHold(subnode, self.clock).bind_to_node(subnode)
            else:
                ZeroOrderHold(node, self.clock).bind_to_node(node)

    def _setup_logger(
        self,
        nodes: List[Node],
        states_to_log: List[str],
        logger_cooldown: float,
        fundamental_step_size: float,
    ) -> None:
        """Set up logging for the graph."""
        if not states_to_log:
            self.logger = None
            return

        self.logger = Logger(
            states_to_log, fundamental_step_size, cooldown=logger_cooldown
        )
        nodes.append(self.logger)

    def _validate_and_set_step_sizes(self, nodes: List[Node]) -> float:
        """Validate and set step sizes for all nodes."""
        defined_step_sizes = [
            node.step_size for node in nodes if node.step_size is not None
        ]
        if not defined_step_sizes:
            raise ValueError("At least one node must have a defined step_size")

        fundamental_step_size = self.define_fundamental_step_size(nodes)
        for node in nodes:
            if node.step_size is None:
                node.step_size = fundamental_step_size

        return fundamental_step_size

    def define_fundamental_step_size(self, nodes: List[Node]) -> float:
        """Define fundamental step size based on node step sizes."""
        step_sizes = [node.step_size for node in nodes if node.step_size is not None]

        def float_gcd(a: float, b: float) -> float:
            precision = 1e-9
            a, b = round(a / precision), round(b / precision)
            return gcd(int(a), int(b)) * precision

        return (
            reduce(float_gcd, step_sizes) if len(set(step_sizes)) > 1 else step_sizes[0]
        )

    def _collect_node_data(self) -> None:
        """Collect inputs and variables from all nodes."""
        provided_vars = {var.full_name for node in self.nodes for var in node.variables}
        external_inputs: List[str] = []

        for node in self.nodes:
            if isinstance(node.inputs, Inputs):
                external_inputs.extend(
                    name for name in node.inputs.inputs if name not in provided_vars
                )

        self.inputs = Inputs(list(set(external_inputs)))

        if any(node.resolved_inputs for node in self.nodes):
            resolved_vars = [
                var
                for node in self.nodes
                if node.resolved_inputs
                for var in node.resolved_inputs.inputs
            ]
            self.resolved_inputs = ResolvedInputs(resolved_vars)

        self._variables = [var for node in self.nodes for var in node.variables]

    def step(self) -> None:
        """Execute all nodes in sequence.

        Executes nodes in dependency order, handling:
        - Multiple step repetitions if configured
        - Proper execution order based on dependencies
        - Time synchronization between nodes
        - Logging of specified states

        The execution respects:
        - Node dependencies (inputs must be computed first)
        - Continuous vs discrete time steps
        - Reset triggers and modifiers
        """
        for _ in range(self.n_step_repeats):
            for node in self.nodes:
                node.step()

    def resolve(self, variables: Sequence[IVariable]) -> Tuple[IInputs, set[str]]:
        """Resolve inputs for all nodes and determine execution order.

        This is a critical setup step that:
        1. Validates variable full name uniqueness across all nodes
        2. Maps dependencies between nodes
        3. Determines correct execution order
        4. Detects circular dependencies

        Args:
            variables: All available variables for resolution

        Returns:
            Tuple of (graph inputs, unresolved variable names)

        Raises:
            ValueError: If duplicate variables or unresolvable dependencies found

        Example:
            ```python
            graph.resolve(graph.variables)  # Setup before execution
            ```
        """
        var_names: Dict[str, Node] = {}
        for node in self.nodes:
            for var in node.variables:
                full_name = var.full_name
                if full_name in var_names:
                    self.resolve_status = ResolveStatus.FAILURE
                    raise ValueError(
                        f"Duplicate variable name found: {full_name}\n"
                        f"First defined in: {var_names[full_name].__class__.__name__}\n"
                        f"Duplicated in: {node.__class__.__name__}"
                    )
                var_names[full_name] = node

        dependencies: Dict[str, Set[str]] = {}
        providers = {
            var.full_name: node for node in self.nodes for var in node.variables
        }

        for node in self.nodes:
            if isinstance(node.inputs, Inputs):
                deps = set()
                for input_name in node.inputs.inputs:
                    if provider := providers.get(input_name):
                        deps.add(provider.external_name)
                dependencies[node.external_name] = deps

        ordered_nodes = self._sort_nodes_by_dependencies(dependencies)
        self.nodes = ordered_nodes

        if self.debug:
            logger.info(f"\nResolved node execution order:\n{self}")

        unresolved: Set[str] = set()
        for node in self.nodes:
            try:
                node.resolve(list(variables))
            except ValueError as e:
                if "Couldn't resolve inputs" in str(e):
                    unresolved.update(
                        str(e)
                        .split("{")[1]
                        .split("}")[0]
                        .strip()
                        .replace("'", "")
                        .split(", ")
                    )

        if unresolved:
            self.resolve_status = ResolveStatus.PARTIAL
            if self.debug:
                self._log_unresolved_inputs(
                    {node.external_name: unresolved for node in self.nodes}
                )
        else:
            self.resolve_status = ResolveStatus.SUCCESS

        self._collect_node_data()

        return self.inputs, unresolved

    def _log_unresolved_inputs(self, unresolved: Dict[str, Set[str]]) -> None:
        """Log information about unresolved inputs."""
        msg = "\nUnresolved inputs found:"
        for node_name, inputs in unresolved.items():
            msg += f"\n{node_name}:"
            for input_name in inputs:
                msg += f"\n  - {input_name}"
        msg += f"\nStatus: {self.resolve_status}"
        logger.info(msg)

    def _sort_nodes_by_dependencies(
        self, dependencies: Dict[str, Set[str]]
    ) -> List[Node]:
        """Sort nodes based on dependencies and root status."""
        root_nodes = [node for node in self.nodes if node.is_root]
        non_root_nodes = [node for node in self.nodes if not node.is_root]
        ordered = []
        visited = set()

        def visit(node: Node) -> None:
            if node.external_name in visited:
                return
            visited.add(node.external_name)

            for dep_name in dependencies.get(node.external_name, set()):
                dep_node = next(n for n in self.nodes if n.external_name == dep_name)
                if not dep_node.is_root:
                    visit(dep_node)

            ordered.append(node)

        ordered.extend(root_nodes)
        visited.update(node.external_name for node in root_nodes)

        for node in non_root_nodes:
            visit(node)

        return ordered

    def insert_node(self, node: Node) -> ResolveStatus:
        """Insert a node into the graph and resolve it."""
        self.nodes.append(node)
        self._collect_node_data()
        if isinstance(node, Graph):
            node._collect_node_data()
            node.resolve(list(node.variables) + list(self.variables))

        self.resolve(list(self.variables))
        return self.resolve_status

    def clone_node(
        self,
        node_name: str,
        new_name: Optional[str] = None,
        defer_resolution: bool = False,
    ) -> Node:
        """Clone a node and its variables."""
        original = next(
            (node for node in self.nodes if node.external_name == node_name),
            None,
        )
        if not original:
            available = "\n- ".join(node.external_name for node in self.nodes)
            raise ValueError(
                f"Node '{node_name}' not found in graph.\nAvailable nodes:\n- {available}"
            )

        memo: Dict[int, Any] = {id(self): self}
        cloned = deepcopy(original, memo)

        if new_name:
            cloned.alter_name(new_name)

        self.nodes.append(cloned)
        if not defer_resolution:
            self._collect_node_data()
            self.resolve(list(self.variables))
        return cloned

    def resolve_all_clones(self) -> None:
        """Batch resolve all cloned nodes at once."""
        self._collect_node_data()
        self.resolve(list(self.variables))

        # Update dependencies for all nodes
        providers = {
            f"{node.external_name}.{var.name}": node
            for node in self.nodes
            for var in node.variables
        }

        for node in self.nodes:
            if isinstance(node.inputs, Inputs):
                new_inputs = []
                for input_name in node.inputs.inputs:
                    provider_name, var_name = input_name.split(".", 1)
                    if f"{provider_name}.{var_name}" in providers:
                        new_inputs.append(input_name)
                    else:
                        base_name = "_".join(provider_name.split("_")[:-1])
                        instance_num = int(provider_name.split("_")[-1])
                        new_provider = f"{base_name}_{instance_num}"
                        new_inputs.append(f"{new_provider}.{var_name}")
                node.inputs = Inputs(new_inputs)
                node.resolved_inputs = None

        # Final resolution pass
        self.resolve(list(self.variables))

    def _update_graph_node_names(self, graph: Graph) -> None:
        """Update names of nodes in a cloned graph."""
        graph_num = int(graph.external_name.split("_")[-1])
        node_mapping = {}
        cloned_bases = set()

        for node in graph.nodes:
            old_name = node.external_name
            base_name = "_".join(old_name.split("_")[:-1])
            new_name = f"{base_name}_{graph_num}"
            node_mapping[old_name] = new_name
            cloned_bases.add(base_name)
            node.alter_name(base_name)

        for node in graph.nodes:
            if isinstance(node.inputs, Inputs):
                new_inputs = []
                for input_name in node.inputs.inputs:
                    provider_name, var_name = input_name.split(".", 1)
                    provider_base = "_".join(provider_name.split("_")[:-1])

                    if provider_name in node_mapping:
                        new_name = node_mapping[provider_name]
                        new_inputs.append(f"{new_name}.{var_name}")
                    elif provider_base in cloned_bases:
                        new_inputs.append(f"{provider_base}_{graph_num}.{var_name}")
                    else:
                        new_inputs.append(input_name)

                node.inputs = Inputs(new_inputs)
                node.resolved_inputs = None

        graph.resolve(graph.variables)
        graph._collect_node_data()

        for node in graph.nodes:
            if not node.is_resolved:
                node.resolve(list(graph.variables))

    def extract_path_as_graph(self, path: str, n_step_repeats: int = 1) -> Graph:
        """Extract a minimal subgraph containing specified nodes."""
        if not path or "->" not in path:
            raise ValueError("Path must be in format: 'node1 -> node2 -> node3'")

        node_names = [name.strip() for name in path.split("->")]
        if not all(node_names):
            raise ValueError("Empty node names are not allowed")

        # Verify nodes exist
        name_to_node = {node.external_name: node for node in self.nodes}
        missing = [name for name in node_names if name not in name_to_node]
        if missing:
            available = "\n- ".join(sorted(name_to_node.keys()))
            raise ValueError(
                f"Could not find nodes: {missing}\nAvailable nodes:\n- {available}"
            )

        # Build dependency graph
        dependencies = self._build_dependency_graph()
        required_nodes = self._find_required_nodes(node_names, dependencies)
        subgraph_nodes = [
            node for node in self.nodes if node.external_name in required_nodes
        ]

        result = Graph(subgraph_nodes, debug=self.debug, n_step_repeats=n_step_repeats)
        return result

    def _build_dependency_graph(self) -> Dict[str, Set[str]]:
        """Build bidirectional dependency graph."""
        dependencies: Dict[str, Set[str]] = {
            node.external_name: set() for node in self.nodes
        }

        for node in self.nodes:
            if isinstance(node.inputs, Inputs):
                for input_name in node.inputs.inputs:
                    for provider in self.nodes:
                        if any(
                            input_name == f"{provider.external_name}.{var.name}"
                            for var in provider.variables
                        ):
                            dependencies[node.external_name].add(provider.external_name)
                            dependencies[provider.external_name].add(node.external_name)

        return dependencies

    def _find_required_nodes(
        self, path_nodes: List[str], dependencies: Dict[str, Set[str]]
    ) -> Set[str]:
        """Find all nodes required for the path."""
        required = set()

        for i in range(len(path_nodes) - 1):
            start, end = path_nodes[i], path_nodes[i + 1]
            if end not in dependencies.get(start, set()):
                path = self._find_path(start, end, dependencies)
                if not path:
                    raise ValueError(f"No path exists between '{start}' and '{end}'")
                required.update(path)
            else:
                required.update([start, end])

        return required

    def _find_path(
        self, start: str, end: str, dependencies: Dict[str, Set[str]]
    ) -> Optional[List[str]]:
        """Find path between two nodes using BFS."""
        visited = set()
        queue = [(start, [start])]

        while queue:
            current, path = queue.pop(0)
            if current == end:
                return path

            for next_node in dependencies.get(current, set()):
                if next_node not in visited:
                    visited.add(next_node)
                    queue.append((next_node, path + [next_node]))

        return None

    def __str__(self) -> str:
        """Return string representation of the graph."""
        nodes_str = "\n".join(
            f"{i:2d}. {node.__class__.__name__:<20} (root={node.is_root}, name={node.external_name})"
            for i, node in enumerate(self.nodes, 1)
        )
        return f"Graph with {len(self.nodes)} nodes:\n{nodes_str}"

    def detect_subgraphs(self) -> List[List[Node]]:
        """Detect independent subgraphs in the node network.

        This method analyzes the dependency structure to:
        1. Find strongly connected components
        2. Identify independent execution groups
        3. Handle root nodes separately

        Returns:
            List of node groups that can be  in principle executed independently

        Example:
            ```python
            subgraphs = graph.detect_subgraphs()
            ```
        """
        subgraphs: List[List[Node]] = []
        used_nodes = set()
        name_to_node = {node.external_name: node for node in self.nodes}

        providers = {
            f"{node.external_name}.{var.name}": node
            for node in self.nodes
            for var in node.variables
        }
        dependencies = self._build_bidirectional_dependencies(providers)
        sccs = self._find_strongly_connected_components(dependencies)

        for scc in sccs:
            group = [name_to_node[name] for name in scc]
            subgraphs.append(group)
            used_nodes.update(scc)

        remaining = [n for n in self.nodes if n.external_name not in used_nodes]

        root_nodes = [
            n
            for n in remaining
            if not isinstance(n.inputs, Inputs) or not n.inputs.inputs
        ]
        if root_nodes:
            subgraphs.append(root_nodes)
            used_nodes.update(n.external_name for n in root_nodes)

        remaining = [n for n in remaining if n.external_name not in used_nodes]
        while remaining:
            node = remaining[0]
            group = [node]
            node_deps = dependencies.get(node.external_name, set())

            for other in remaining[1:]:
                if dependencies.get(other.external_name, set()) == node_deps:
                    group.append(other)

            subgraphs.append(group)
            used_nodes.update(n.external_name for n in group)
            remaining = [n for n in remaining if n.external_name not in used_nodes]

        if self.debug:
            self._log_subgraph_analysis(subgraphs)

        return subgraphs

    def _build_bidirectional_dependencies(
        self, providers: Dict[str, Node]
    ) -> Dict[str, Set[str]]:
        """Build bidirectional dependency graph."""
        dependencies: Dict[str, Set[str]] = {
            node.external_name: set() for node in self.nodes
        }

        for node in self.nodes:
            if isinstance(node.inputs, Inputs):
                for input_name in node.inputs.inputs:
                    if provider := providers.get(input_name):
                        dependencies[node.external_name].add(provider.external_name)
                        dependencies[provider.external_name].add(node.external_name)

        return dependencies

    def _find_strongly_connected_components(
        self, dependencies: Dict[str, Set[str]]
    ) -> List[List[str]]:
        """Find strongly connected components using Tarjan's algorithm."""
        index: Dict[str, int] = {}
        lowlink: Dict[str, int] = {}
        stack: List[str] = []
        on_stack: Set[str] = set()
        sccs: List[List[str]] = []

        for node in self.nodes:
            if node.external_name not in index:
                _, new_sccs = find_scc(
                    node.external_name,
                    stack,
                    index,
                    lowlink,
                    on_stack,
                    0,
                    dependencies=dependencies,
                )
                sccs.extend(new_sccs)

        return sccs

    def extract_as_subgraph(
        self, node_names: List[str], n_step_repeats: int = 1
    ) -> Graph:
        """Extract specified nodes into a single subgraph node.

        This method supports hierarchical composition by:
        1. Creating a new graph from selected nodes
        2. Maintaining proper dependencies
        3. Supporting nested parallelization

        Args:
            node_names: Names of nodes to include in subgraph
            n_step_repeats: Number of times to repeat step execution

        Returns:
            New graph containing specified nodes

        Example:
            ```python
            # Create hierarchical structure
            fast_graph = graph.extract_as_subgraph(
                ["sensor1", "controller1"],
                n_step_repeats=10
            )
            ```

        Raises:
            ValueError: If specified nodes don't exist
        """
        name_to_node = {node.external_name: node for node in self.nodes}
        missing = [name for name in node_names if name not in name_to_node]
        if missing:
            available = "\n- ".join(sorted(name_to_node.keys()))
            raise ValueError(
                f"Could not find nodes: {missing}\nAvailable nodes:\n- {available}"
            )

        subgraph_nodes = [
            node for node in self.nodes if node.external_name in node_names
        ]
        subgraph = Graph(
            subgraph_nodes, debug=self.debug, n_step_repeats=n_step_repeats
        )

        self.nodes = [
            node for node in self.nodes if node.external_name not in node_names
        ]
        self.insert_node(subgraph)
        return subgraph

    def _log_subgraph_analysis(self, subgraphs: List[List[Node]]) -> None:
        """Log detailed subgraph analysis."""
        logger.info("\nSubgraph Analysis:")
        for i, group in enumerate(subgraphs):
            logger.info(f"\nGroup {i}:")
            logger.info("  Nodes:")
            for node in group:
                logger.info(f"    {node.__class__.__name__}({node.external_name})")
            logger.info("  Consumes:")
            for node in group:
                if isinstance(node.inputs, Inputs):
                    logger.info(f"    {node.external_name}: {node.inputs.inputs}")
            logger.info("  Provides:")
            for node in group:
                vars_node = [f"{node.external_name}.{v.name}" for v in node.variables]
                logger.info(f"    {node.external_name}: {vars_node}")

    def print_subgraphs(self, subgraphs: List[List[Node]]) -> None:
        """Print detected subgraphs in a readable format."""
        logger.info("\nDetected parallel execution groups:")
        for i, subgraph in enumerate(subgraphs, 1):
            nodes_str = "\n  ".join(
                f"- {node.__class__.__name__:<20} (root={node.is_root}, name={node.external_name})"
                for node in subgraph
            )
            logger.info(f"\nGroup {i}:\n  {nodes_str}")

    def analyze_group_dependencies(
        self, subgraphs: List[List[Node]]
    ) -> Dict[int, Set[int]]:
        """Analyze dependencies between groups."""
        var_to_group = {}
        group_contents = {}

        for group_idx, nodes in enumerate(subgraphs):
            group_contents[group_idx] = [node.__class__.__name__ for node in nodes]
            for node in nodes:
                for var in node.variables:
                    var_to_group[f"{node.external_name}.{var.name}"] = group_idx

                if isinstance(node.inputs, Inputs):
                    for input_name in node.inputs.inputs:
                        original_name = next(
                            (
                                old
                                for old, new in getattr(
                                    node, "_variable_mapping", {}
                                ).items()
                                if new == input_name
                            ),
                            input_name,
                        )
                        var_to_group[original_name] = group_idx

        group_deps: Dict[int, Set[int]] = {}

        if self.debug:
            self._log_group_dependencies(subgraphs, group_contents)

        for group_idx, nodes in enumerate(subgraphs):
            for node in nodes:
                if isinstance(node.inputs, Inputs):
                    for input_name in node.inputs.inputs:
                        if provider_group := var_to_group.get(input_name):
                            if provider_group != group_idx:
                                group_deps[group_idx].add(provider_group)

        return group_deps

    def _log_group_dependencies(
        self, subgraphs: List[List[Node]], group_contents: Dict[int, List[str]]
    ) -> None:
        """Log group dependency information."""
        logger.info("\nVariable providers and consumers:")
        for group_idx, nodes in enumerate(subgraphs):
            logger.info(
                f"\nGroup {group_idx} ({', '.join(group_contents[group_idx])}):"
            )
            for node in nodes:
                if isinstance(node.inputs, Inputs):
                    logger.info(
                        f"  {node.__class__.__name__} consumes: {node.inputs.inputs}"
                    )

    def reset(self, *, apply_reset_modifier: bool = True) -> None:
        """Reset the graph and its nodes to their initial states.

        Args:
            apply_reset_modifier: Whether to apply reset modifier if available.
        """
        if apply_reset_modifier and self._modified_reset is not None:
            self._modified_reset()
            return

        for node in self.nodes:
            node.reset(apply_reset_modifier=apply_reset_modifier)

    def reset_nodes(
        self,
        nodes_to_reset: Optional[List[Node]] = None,
        apply_reset_modifier_to: Optional[List[Node]] = None,
    ) -> None:
        """Reset specific nodes in the graph.

        Args:
            nodes_to_reset: List of nodes to reset. If None, resets all nodes.
            apply_reset_modifier_to: List of nodes to apply reset modifier to. If None, follows default behavior.
        """
        target_nodes = nodes_to_reset if nodes_to_reset is not None else self.nodes

        for node in target_nodes:
            should_apply_modifier = (
                apply_reset_modifier_to is None or node in apply_reset_modifier_to
            )
            node.reset(apply_reset_modifier=should_apply_modifier)

    def print_info(self, indent: int = 0) -> str:
        """Print detailed information about all nodes in the graph."""
        lines = []
        prefix = "  " * indent
        lines.append(f"{prefix}Graph: {self.external_name}")

        for node in self.nodes:
            if isinstance(node, Graph):
                lines.append(node.print_info(indent + 1))
            else:
                lines.append(f"{prefix}  Node: {node.__class__.__name__}")
                lines.append(f"{prefix}    External name: {node.external_name}")
                if isinstance(node.inputs, Inputs):
                    lines.append(f"{prefix}    Inputs: {node.inputs.inputs}")
                if node.resolved_inputs:
                    resolved = [var.full_name for var in node.resolved_inputs.inputs]
                    lines.append(f"{prefix}    Resolved inputs: {resolved}")

        msg = "\n".join(lines)
        if indent == 0:
            logger.info(msg)
        return msg

    def get_full_names(self) -> List[str]:
        """Get fully qualified names of all variables.

        Returns:
            List of strings in format 'node_name.variable_name'.
        """
        return [name for node in self.nodes for name in node.get_full_names()]

    def __deepcopy__(self, memo: Dict[Any, Any]) -> Graph:
        """Custom deepcopy implementation to handle graph context."""
        if id(self) in memo:
            return memo[id(self)]

        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result

        result._internal_name = self._internal_name
        result._external_name = (
            f"{result._internal_name}_{len(cls._instances[cls.__name__])}"
        )

        for k, v in self.__dict__.items():
            if k not in [
                "_external_name",
                "_variables",
                "_inputs",
                "_nodes",
            ]:
                setattr(result, k, deepcopy(v, memo))
            elif k == "_resolved_inputs":
                setattr(result, k, None)

        result.nodes = []

        node_mapping = {}
        internal_nodes = set()

        for node in self.nodes:
            if id(node) in memo:
                cloned_node = memo[id(node)]
            else:
                cloned_node = deepcopy(node, memo)
                memo[id(node)] = cloned_node
            result.nodes.append(cloned_node)
            if isinstance(node, Graph):
                for node_inner, node_corresponding in zip(
                    node.nodes, cloned_node.nodes
                ):
                    node_mapping[node_inner.external_name] = node_corresponding
                    internal_nodes.add(node_corresponding._internal_name)
            else:
                node_mapping[node.external_name] = cloned_node
                internal_nodes.add(cloned_node._internal_name)

        for node in result.nodes:
            if isinstance(node, Graph):
                for node_inner in node.nodes:
                    self._map_new_inputs(node_inner, node_mapping, internal_nodes)
                node._collect_node_data()
            else:
                self._map_new_inputs(node, node_mapping, internal_nodes)

        result._collect_node_data()

        return result

    def _map_new_inputs(
        self, node: Node, node_mapping: Dict[str, Node], internal_nodes: Set[str]
    ) -> None:
        new_inputs = []
        for input_name in node.inputs.inputs:
            provider_name, var_name = input_name.split(".", 1)
            provider_base = provider_name.rsplit("_", 1)[0]
            if provider_name in node_mapping:
                new_inputs.append(
                    f"{node_mapping[provider_name].external_name}.{var_name}"
                )
            elif provider_base in internal_nodes:
                new_provider_name = f"{provider_base}_{len(node_mapping)}"
                new_inputs.append(f"{new_provider_name}.{var_name}")
            else:
                new_inputs.append(input_name)
        node.inputs = Inputs(new_inputs)

    def parallelize(self, **kwargs: Any) -> ParallelGraph:
        """Convert to parallel execution mode."""
        from regelum.node.parallel import ParallelGraph

        return ParallelGraph(self.nodes, self.debug, **kwargs)

    def add_node(self, node: Node) -> None:
        """Add a node to the graph."""
        self.nodes.append(node)
        self._collect_node_data()

    def remove_node(self, node: Node) -> None:
        """Remove a node from the graph."""
        self.nodes.remove(node)
        self._collect_node_data()

    @property
    def clock(self) -> Clock:
        """Get the clock node."""
        if self._clock is None:
            raise ValueError("Clock not initialized")
        return self._clock
