"""Global mutable variables are stored here."""

from __future__ import annotations

from typing import TYPE_CHECKING

import tcod.console
import tcod.context
import tcod.ecs

if TYPE_CHECKING:
    import game.state

context: tcod.context.Context
console: tcod.console.Console
states: list[game.state.State] = []
world: tcod.ecs.World
