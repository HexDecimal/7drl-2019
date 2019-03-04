from typing import Any, List, Tuple, TYPE_CHECKING

import engine.component
if TYPE_CHECKING:
    import engine.entity
    import engine.zone


class Location(engine.component.Component):
    # Remove the zone property from Component.
    zone: "engine.zone.Zone" = None  # type: ignore

    def __init__(self, zone: "engine.zone.Zone", xyz: Tuple[int, int, int]):
        self.zone = zone
        self.xyz = xyz
        self.contents: List[engine.entity.Entity] = []

    def on_added(self, entity: "engine.entity.Entity") -> None:
        assert entity not in self.contents
        self.contents.append(entity)
        if entity.actor:
            entity.actor.schedule(0)

    def on_replace(
        self,
        entity: "engine.entity.Entity",
        old: "Location"
    ) -> None:
        assert self.zone is old.zone
        old.contents.remove(entity)
        self.contents.append(entity)

    def on_destroy(self, entity: "engine.entity.Entity") -> None:
        self.contents.remove(entity)

    def get_relative(self, x: int, y: int, z: int = 0) -> "Location":
        """Return a location relative to this one."""
        return self.zone[self.xyz[0] + x, self.xyz[1] + y, self.xyz[2] + z]

    @property
    def data(self) -> Any:
        return self.zone.data[self.xyz]
