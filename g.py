"""Global mutable variables are stored here."""
from __future__ import annotations

import tcod.console
import tcod.context
import tcod.ecs

context: tcod.context.Context
console: tcod.console.Console
world: tcod.ecs.World
