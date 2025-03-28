"""Reset modifier implementation module."""

from typing import Any

from regelum.node.modifiers.base import StepModifier
from regelum.node.base import Node


class ResetOnStep(StepModifier[Node]):
    """Modifier that adds reset behavior to a node based on a semaphore."""

    def __init__(self, node: Node, reset_semaphore: Node) -> None:
        """Initialize reset modifier.

        Args:
            node: Node to modify.
            reset_semaphore: Node that triggers resets.
        """
        super().__init__()
        if (
            "_".join(reset_semaphore.external_name.split("_")[1:-1])
            != node.external_name
        ):
            raise ValueError(
                f"Reset semaphore {'_'.join(reset_semaphore.external_name.split('_')[1:-1])} must be the same as the node {node.external_name}."
            )
        self._node = node
        self._step_function = node.step
        self._reset_semaphore = reset_semaphore

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        """Execute modified step with reset check."""
        if self._reset_semaphore.get_variable("flag").value:
            self._node.reset(apply_reset_modifier=True)
            return
        self._step_function(*args, **kwargs)

    def reset(self, *, apply_reset_modifier: bool = True) -> None:
        """Reset the node's state."""
        self._node.reset(apply_reset_modifier=apply_reset_modifier)
