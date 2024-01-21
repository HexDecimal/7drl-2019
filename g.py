from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import tcod.console
    import tcod.context

    import engine.model

context: tcod.context.Context
console: tcod.console.Console
model: engine.model.Model
