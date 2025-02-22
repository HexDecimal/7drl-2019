"""Common components."""

from __future__ import annotations

from typing import TYPE_CHECKING, Final, Protocol

import tcod.ecs

if TYPE_CHECKING:
    from game.action import ActionResult

Name: Final = ("Name", str)
"""The name of an entity."""

MoveSpeed: Final = ("MoveSpeed", int)
AttackSpeed: Final = ("AttackSpeed", int)


MessageLog: Final = ("log", list[str])
"""Log of recorded messages."""


class Interactable(Protocol):
    """Handle simple bump interactions."""

    def __call__(self, issuer: tcod.ecs.Entity, target: tcod.ecs.Entity, /) -> ActionResult:
        """Called when the player/issuer bumps into target."""
        ...
