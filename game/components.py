"""Common components."""

from __future__ import annotations

from typing import TYPE_CHECKING, Final, Protocol

import attrs
import tcod.ecs

if TYPE_CHECKING:
    from game.action import ActionResult

Name: Final = ("Name", str)
"""The name of an entity."""

MoveSpeed: Final = ("MoveSpeed", int)
AttackSpeed: Final = ("AttackSpeed", int)


MessageLog: Final = ("log", list[str])
"""Log of recorded messages."""

Shape3D = ("Shape3D", tuple[int, int, int])


class Interactable(Protocol):
    """Handle simple bump interactions."""

    def __call__(self, issuer: tcod.ecs.Entity, target: tcod.ecs.Entity, /) -> ActionResult:
        """Called when the player/issuer bumps into target."""
        ...


@attrs.define(frozen=True)
class Graphic:
    """Entity glyph graphic."""

    ch: int = ord("!")
    fg: tuple[int, int, int] = (255, 255, 255)
    priority: int = 0

    def get(self) -> tuple[int, tuple[int, int, int]]:
        """Return `(ch, fg)`."""
        return self.ch, self.fg
