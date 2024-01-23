from __future__ import annotations

from typing import Protocol

import tcod.ecs


class ActionLike(Protocol):
    entity: tcod.ecs.Entity

    def invoke(self) -> bool:
        """Attempt the action and return True if the action was performed."""

    def poll(self) -> ActionLike | None:
        """Return an action which would be valid."""

    def action(self) -> int | None:
        """Perform the action.

        This should never be called unless poll returns True.
        """
