from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import tcod.console
    import engine.world
    import engine.entity

console: "tcod.console.Console"
player: "engine.entity.Entity"
world: "engine.world.World"
