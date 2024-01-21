from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import tcod.console
    import engine.model
    import tcod.context

context: tcod.context.Context
console: tcod.console.Console
model: engine.model.Model
