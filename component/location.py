from __future__ import annotations

from typing import TYPE_CHECKING, Self

import attrs
import tcod.ecs
import tcod.ecs.callbacks

if TYPE_CHECKING:
    import engine.zone


@attrs.define(frozen=True)
class Location:
    """A tile location within a specific zone."""

    x: int = attrs.field(converter=int)
    y: int = attrs.field(converter=int)
    z: int = attrs.field(converter=int)
    zone: engine.zone.Zone

    def replace(
        self,
        x: int | None = None,
        y: int | None = None,
        z: int | None = None,
        *,
        zone: engine.zone.Zone | None = None,
    ) -> Self:
        """Return a copy with the given parameters replaced."""
        return self.__class__(
            zone=zone if zone is not None else self.zone,
            x=x if x is not None else self.x,
            y=y if y is not None else self.y,
            z=z if z is not None else self.z,
        )

    def is_adjacent(self, other: Location) -> bool:
        """Return True if this location is at most one tile away from `other`."""
        if self.z != other.z:
            return False
        if abs(self.x - other.x) > 1:
            return False
        if abs(self.y - other.y) > 1:  # noqa: SIM103
            return False
        return True

    @property
    def xyz(self) -> tuple[int, int, int]:
        """Return the coordinates of this location."""
        return self.x, self.y, self.z

    @property
    def ijk(self) -> tuple[int, int, int]:
        """Return the ijk coordinates of this location."""
        return self.z, self.y, self.x

    def __add__(self, other: tuple[int, int, int]) -> Location:
        """Return a location relative to this one."""
        x, y, z = other
        return self.__class__(self.x + x, self.y + y, self.z + z, self.zone)


@tcod.ecs.callbacks.register_component_changed(component=Location)
def on_location_changed(entity: tcod.ecs.Entity, old: Location | None, new: Location | None) -> None:
    """Track location changes."""
    if old == new:
        return
    if old is not None:
        entity.tags.remove(old)
    if new is not None:
        entity.tags.add(new)
