from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import tcod.console
    import engine.zone
    import obj.entity

console: "tcod.console.Console"
player: "obj.entity.Entity"
zone: "engine.zone.Zone"
