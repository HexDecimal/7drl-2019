from __future__ import annotations

from typing import Tuple, TYPE_CHECKING

from component.location import List, Location
if TYPE_CHECKING:
    from obj.entity import Entity
    import engine.zone


class Container(Location):
    owner: Entity
    capacity = 100

    def __init__(self) -> None:
        self.contents: List[Entity] = []

    def on_added(self, entity: Entity) -> None:
        if not hasattr(self, "owner"):
            self.owner = entity
        else:
            super().on_added(entity)

    def on_destroy(self, entity: Entity) -> None:
        for obj in list(self.contents):
            obj.location = self.owner.location
        super().on_destroy(entity)

    @property
    def zone(self) -> engine.zone.Zone:
        return self.owner.location.zone

    @property
    def xyz(self) -> Tuple[int, int, int]:
        return self.owner.location.xyz
