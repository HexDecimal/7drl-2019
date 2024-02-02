"""Global mutable variables are stored here."""
from __future__ import annotations

import tcod.console
import tcod.context
import tcod.ecs

import game.state

context: tcod.context.Context
console: tcod.console.Console
states: list[game.state.State] = []
world: tcod.ecs.World
