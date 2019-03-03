from typing import List, Tuple

import engine.component
import engine.entity
import engine.world


class Location(engine.component.Component):
    # Remove the world property from Component.
    world: "engine.world.World" = None  # type: ignore

    def __init__(self, world: "engine.world.World", xyz: Tuple[int, int, int]):
        self.world = world
        self.xyz = xyz
        self.contents: List[engine.entity.Entity] = []

    def on_added(self, entity: "engine.entity.Entity") -> None:
        assert entity not in self.contents
        self.contents.append(entity)

    def on_remove(self, entity: "engine.entity.Entity") -> None:
        self.contents.remove(entity)

    def get_relative(self, x: int, y: int, z: int = 0) -> "Location":
        """Return a location relative to this one."""
        return self.world[self.xyz[0] + x, self.xyz[1] + y, self.xyz[2] + z]
