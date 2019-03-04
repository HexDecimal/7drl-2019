from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import tcod.console
    import engine.world

console: "tcod.console.Console"
world: "engine.world.World"
