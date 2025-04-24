"""Rendering logic."""

import tcod.console
import tcod.ecs

from component.location import Location
from engine.zone import Zone
from game.components import Graphic, Shape3D


def render_zone(entity: tcod.ecs.Entity, console: tcod.console.Console) -> None:
    """Render a zone to a console."""
    zone = entity.components[Zone]
    console.clear()
    cam_x, cam_y, cam_z = entity.registry["camera"].components[Location].xyz
    cam_x -= console.width // 2
    cam_y -= console.height // 2

    width, height, depth = entity.components[Shape3D]

    cam_left = max(0, cam_x)
    cam_top = max(0, cam_y)
    cam_right = min(cam_x + console.width, width)
    cam_bottom = min(cam_y + console.height, height)

    con_view = (slice(cam_left - cam_x, cam_right - cam_x), slice(cam_top - cam_y, cam_bottom - cam_y))

    tile = zone.data["tile"][cam_left:cam_right, cam_top:cam_bottom, cam_z]

    console.rgb.T["ch"][con_view] = tile["ch"]
    console.rgb.T["fg"][con_view] = tile["fg"]
    console.rgb.T["bg"][con_view] = tile["bg"]

    console_ch_fg = console.rgb[["ch", "fg"]]

    for e in entity.registry.Q.all_of(components=[Graphic, Location]):
        loc = e.components[Location]
        x = loc.x - cam_x
        y = loc.y - cam_y
        if 0 <= x < console.width and 0 <= y < console.height:
            console_ch_fg[y, x] = e.components[Graphic].get()
