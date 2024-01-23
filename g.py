"""Global mutable variables are stored here."""
from __future__ import annotations

from typing import TYPE_CHECKING

import tcod.console
import tcod.context
import tcod.ecs

if TYPE_CHECKING:
    import engine.model

context: tcod.context.Context
console: tcod.console.Console
model: engine.model.Model
world: tcod.ecs.World
