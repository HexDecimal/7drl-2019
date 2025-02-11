"""Action base types."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, TypeAlias

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

    if not TYPE_CHECKING:
        __slots__ = ()

    def __call__(self, entity: tcod.ecs.Entity, /) -> ActionResult:
        """Action call parameters."""
        ...
