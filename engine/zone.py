from __future__ import annotations

from typing import TYPE_CHECKING, Final

import numpy as np
import tcod.console
import tcod.ecs

import component.actor
import component.location
import engine.helpers
import g
import tiles
from component.graphic import Graphic
from game.action import Action
from game.tags import IsControlled
from game.typing import TurnQueue_

if TYPE_CHECKING:
    import procgen.shipgen


class Zone:
    DTYPE: Final = [("tile", tiles.DTYPE), ("room_id", np.int16)]
    locations: dict[tuple[int, int, int], component.location.Location]
    room_types: dict[int, procgen.shipgen.RoomType]

    def __init__(self, shape: tuple[int, int, int]) -> None:
        self.shape = shape

        self.camera: tuple[int, int, int] = (0, 0, 0)

        self.data = np.empty(shape, dtype=self.DTYPE, order="F")
        self.data["tile"] = tiles.metal_wall
        self.data["tile"][1:-1, 1:-1, :] = tiles.metal_floor

        self.locations = {}

    def simulate(self) -> None:
        while not g.world.Q.all_of(tags=[IsControlled]):
            ticket = g.world[None].components[TurnQueue_].pop()
            component.actor.Actor.call(ticket, ticket.value)
            if component.actor.Actor not in engine.helpers.active_player().components:
                msg = "Player has died."
                raise SystemExit(msg)
        for entity in g.world.Q.all_of(tags=[IsControlled]):
            entity.components.pop(Action, None)  # Clear PlayerControl action.

    def render(self, console: tcod.console.Console) -> None:
        console.clear()
        cam_x, cam_y, cam_z = self.camera
        cam_x -= console.width // 2
        cam_y -= console.height // 2

        cam_left = max(0, cam_x)
        cam_top = max(0, cam_y)
        cam_right = min(cam_x + console.width, self.width)
        cam_bottom = min(cam_y + console.height, self.height)

        con_view = (slice(cam_left - cam_x, cam_right - cam_x), slice(cam_top - cam_y, cam_bottom - cam_y))

        tile = self.data["tile"][cam_left:cam_right, cam_top:cam_bottom, cam_z]

        console.ch[con_view] = tile["ch"]
        console.fg[con_view] = tile["fg"]
        console.bg[con_view] = tile["bg"]

        for entity in g.world.Q.all_of(components=[Graphic, component.location.Location]):
            loc = entity.components[component.location.Location]
            x = loc.x - cam_x
            y = loc.y - cam_y
            if 0 <= x < console.width and 0 <= y < console.height:
                console.ch[x, y], console.fg[x, y] = entity.components[Graphic].get()

    def __getitem__(
        self,
        xyz: tuple[int, int, int],
    ) -> component.location.Location:
        """Return a location, creating a new one if it doesn't exist."""
        if xyz not in self.locations:
            self.locations[xyz] = component.location.Location(self, *xyz)
        return self.locations[xyz]

    @property
    def width(self) -> int:
        return self.shape[0]

    @property
    def height(self) -> int:
        return self.shape[1]

    @property
    def depth(self) -> int:
        return self.shape[2]
