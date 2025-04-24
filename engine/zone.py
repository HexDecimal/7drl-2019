from __future__ import annotations

from typing import TYPE_CHECKING, Final

import numpy as np
import tcod.ecs

import component.location
import tiles
from game.components import Shape3D

if TYPE_CHECKING:
    import procgen.shipgen


class Zone:
    DTYPE: Final = [("tile", tiles.DTYPE), ("room_id", np.int16)]
    room_types: dict[int, procgen.shipgen.RoomType]

    def __init__(self, entity: tcod.ecs.Entity, shape: tuple[int, int, int]) -> None:
        self.entity = entity
        entity.components[Shape3D] = shape

        self.data = np.empty(shape, dtype=self.DTYPE, order="F")
        self.data["tile"] = tiles.metal_wall
        self.data["tile"][1:-1, 1:-1, :] = tiles.metal_floor

    def __getitem__(
        self,
        xyz: tuple[int, int, int],
    ) -> component.location.Location:
        """Return a location, creating a new one if it doesn't exist."""
        return component.location.Location(*xyz, zone=self)
