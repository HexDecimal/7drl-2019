from __future__ import annotations

from typing import Tuple, TYPE_CHECKING

from component.base import OwnedComponent
from component.location import List, Location
if TYPE_CHECKING:
    from obj.entity import Entity
    import engine.zone


class ContainerLocation(Location):
    def __init__(self, master: Container) -> None:
        self.master = master
        self.contents: List[Entity] = []

    @property
    def zone(self) -> engine.zone.Zone:
        return self.master.owner.location.zone

    @property
    def xyz(self) -> Tuple[int, int, int]:
        return self.master.owner.location.xyz


class Container(OwnedComponent):

    def __init__(self) -> None:
        super().__init__()
        self.container = ContainerLocation(self)

    @property
    def contents(self) -> List[Entity]:
        return self.container.contents
