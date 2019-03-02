from typing import Any, Dict, Optional, Tuple

import tqueue

import engine.entity
import engine.location


class World:
    DTYPE: Any = []
    locations: Dict[Tuple[int, int, int], engine.location.Location]

    def __init__(self, width: int, height: int, depth: int = 1) -> None:
        self.width = width
        self.height = height
        self.depth = depth

        self.locations = {}
        self.tqueue = tqueue.TurnQueue()

        self.player: Optional[engine.entity.Entity] = None

    def simulate(self) -> None:
        while not self.player:
            self.tqueue.next().value()

    def __getitem__(
        self,
        xyz: Tuple[int, int, int],
    ) -> engine.location.Location:
        """Return a location, creating a new one if it doesn't exist."""
        if xyz not in self.locations:
            self.locations[xyz] = engine.location.Location(self, xyz)
        return self.locations[xyz]
