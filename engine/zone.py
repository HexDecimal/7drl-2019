from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

import numpy as np
import tcod
import tqueue

import obj.entity
import component.location
import tiles


class Zone:
    DTYPE: Any = [("tile", tiles.DTYPE)]
    locations: Dict[Tuple[int, int, int], component.location.Location]

    def __init__(self, shape: Tuple[int, int, int]) -> None:
        self.shape = shape

        self.camera = (0, 0, 0)

        self.data = np.empty(shape, dtype=self.DTYPE, order="F")
        self.data["tile"] = tiles.metal_wall
        self.data["tile"][1:-1, 1:-1, :] = tiles.metal_floor

        self.locations = {}
        self.tqueue = tqueue.TurnQueue()

        self.player: Optional[obj.entity.Entity] = None

    def simulate(self) -> None:
        while not self.player:
            ticket = self.tqueue.next()
            ticket.value(ticket)
        assert self.player.actor
        self.player.actor.action = None  # Clear PlayerControl action.

    def render(self, console: tcod.console.Console) -> None:
        console.clear()
        cam_x, cam_y, cam_z = self.camera
        cam_x -= console.width // 2
        cam_y -= console.height // 2

        cam_left = max(0, cam_x)
        cam_top = max(0, cam_y)
        cam_right = min(cam_x + console.width, self.width)
        cam_bottom = min(cam_y + console.height, self.height)

        con_view = (slice(cam_left - cam_x, cam_right - cam_x),
                    slice(cam_top - cam_y, cam_bottom - cam_y))

        tile = self.data["tile"][cam_left:cam_right, cam_top:cam_bottom, cam_z]

        console.ch[con_view] = tile["ch"]
        console.fg[con_view] = tile["fg"]
        console.bg[con_view] = tile["bg"]

        for y in range(console.height):
            for x in range(console.width):
                for entity in self[x + cam_x, y + cam_y, cam_z].contents:
                    if not entity.graphic:
                        continue
                    console.ch[x, y], console.fg[x, y] = entity.graphic.get()

    def __getitem__(
        self,
        xyz: Tuple[int, int, int],
    ) -> component.location.Location:
        """Return a location, creating a new one if it doesn't exist."""
        if xyz not in self.locations:
            self.locations[xyz] = component.location.Location(self, xyz)
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
