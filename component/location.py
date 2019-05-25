from __future__ import annotations

from typing import Any, List, Tuple, TYPE_CHECKING

import component.base

if TYPE_CHECKING:
    import obj.entity
    import engine.zone


class Location(component.base.Component):
    def __init__(self, zone: engine.zone.Zone, xyz: Tuple[int, int, int]):
        self._zone = zone
        self._xyz = xyz
        self.contents: List[obj.entity.Entity] = []

    def on_added(self, entity: obj.entity.Entity) -> None:
        assert entity not in self.contents
        self.contents.append(entity)

    def on_replace(
        self,
        entity: obj.entity.Entity,
        old: Location
    ) -> None:
        assert self.zone is old.zone
        old.contents.remove(entity)
        self.contents.append(entity)

    def on_remove(self, entity: obj.entity.Entity) -> None:
        assert entity in self.contents
        self.contents.remove(entity)

    def on_destroy(self, entity: obj.entity.Entity) -> None:
        self.contents.remove(entity)

    def get_relative(self, x: int, y: int, z: int = 0) -> Location:
        """Return a location relative to this one."""
        return self.zone[self.xyz[0] + x, self.xyz[1] + y, self.xyz[2] + z]

    def is_adjacent(self, other: Location) -> bool:
        """Return True if this location is at most one tile away from `other`.
        """
        if self.xyz[2] != other.xyz[2]:
            return False
        if abs(self.xyz[0] - other.xyz[0]) > 1:
            return False
        if abs(self.xyz[1] - other.xyz[1]) > 1:
            return False
        return True

    @property
    def data(self) -> Any:
        return self.zone.data[self.xyz]

    @property
    def xyz(self) -> Tuple[int, int, int]:
        return self._xyz

    @property
    def zone(self) -> engine.zone.Zone:
        return self._zone
