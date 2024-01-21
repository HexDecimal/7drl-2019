from __future__ import annotations

from typing import TYPE_CHECKING

from component.base import OwnedComponent
from component.location import Location

if TYPE_CHECKING:
    import engine.zone
    from obj.entity import Entity


class ContainerLocation(Location):
    def __init__(self, master: Container) -> None:
        self.master = master
        self.contents: list[Entity] = []

    @property
    def zone(self) -> engine.zone.Zone:
        return self.master.owner.location.zone

    @property
    def xyz(self) -> tuple[int, int, int]:
        return self.master.owner.location.xyz


class Container(OwnedComponent):
    def __init__(self) -> None:
        super().__init__()
        self.container = ContainerLocation(self)

    @property
    def contents(self) -> list[Entity]:
        return self.container.contents
