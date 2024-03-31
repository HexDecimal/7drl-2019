from __future__ import annotations

from typing import Protocol, TypeAlias

import attrs
import tcod.ecs


@attrs.define
class Success:
    """Action performed successfully."""

    time_cost: int = 100


@attrs.define
class Impossible:
    """Action can not be performed."""

    reason: str

    def __bool__(self) -> bool:
        """Impossible results are falsy."""
        return False


ActionResult: TypeAlias = Success | Impossible  # noqa: UP040


class Action(Protocol):
    """Base action protocol."""

    __slots__ = ()

    def perform(self, entity: tcod.ecs.Entity) -> ActionResult:
        """Action call parameters."""


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
