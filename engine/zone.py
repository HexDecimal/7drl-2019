from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import tcod.ecs

import component.location
import tiles
from game.components import RoomIDArray, Shape3D, TileData

if TYPE_CHECKING:
    import procgen.shipgen


class Zone:
    room_types: dict[int, procgen.shipgen.RoomType]

    def __init__(self, entity: tcod.ecs.Entity, shape: tuple[int, int, int]) -> None:
        self.entity = entity
        entity.components[Shape3D] = shape

        entity.components[TileData] = tiles_ = np.zeros(shape, dtype=tiles.DTYPE)
        tiles_[:] = tiles.metal_wall
        tiles_.T[1:-1, 1:-1, :] = tiles.metal_floor

        entity.components[RoomIDArray] = np.zeros(shape, dtype=np.int16)

    def __getitem__(
        self,
        xyz: tuple[int, int, int],
    ) -> component.location.Location:
        """Return a location, creating a new one if it doesn't exist."""
        return component.location.Location(*xyz, zone=self.entity)
