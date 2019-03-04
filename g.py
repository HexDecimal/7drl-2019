from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import tcod.console
    import engine.zone
    import engine.entity

console: "tcod.console.Console"
player: "engine.entity.Entity"
zone: "engine.zone.Zone"
