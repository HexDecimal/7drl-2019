from __future__ import annotations

from typing import TYPE_CHECKING, Any

import attrs
import tcod.ecs
import tcod.ecs.callbacks

if TYPE_CHECKING:
    import engine.zone


@attrs.define(frozen=True)
class Location:
    zone: engine.zone.Zone
    x: int
    y: int
    z: int

    def get_relative(self, x: int, y: int, z: int = 0) -> Location:
        """Return a location relative to this one."""
        return Location(self.zone, self.x + x, self.y + y, self.z + z)

    def is_adjacent(self, other: Location) -> bool:
        """Return True if this location is at most one tile away from `other`."""
        if self.z != other.z:
            return False
        if abs(self.x - other.x) > 1:
            return False
        if abs(self.y - other.y) > 1:
            return False
        return True

    @property
    def xyz(self) -> tuple[int, int, int]:
        return self.x, self.y, self.z

    @property
    def data(self) -> Any:
        return self.zone.data[self.x, self.y, self.z]

    def __add__(self, other: tuple[int, int, int]) -> Location:
        """Return a location relative to this one."""
        x, y, z = other
        return self.__class__(self.zone, self.x + x, self.y + y, self.z + z)


@tcod.ecs.callbacks.register_component_changed(component=Location)
def on_location_changed(entity: tcod.ecs.Entity, old: Location | None, new: Location | None) -> None:
    if old == new:
        return
    if old is not None:
        entity.tags.remove(old)
    if new is not None:
        entity.tags.add(new)
