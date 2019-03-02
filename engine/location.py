from typing import List, Tuple

import engine.entity
import engine.world


class Location:

    def __init__(self, world: "engine.world.World", xyz: Tuple[int, int, int]):
        self.world = world
        self.xyz = xyz
        self.contents: List[engine.entity.Entity] = []

    def get_relative(self, x: int, y: int, z: int = 0) -> "Location":
        """Return a location relative to this one."""
        return self.world[self.xyz[0] + x, self.xyz[1] + y, self.xyz[2] + z]
