from __future__ import annotations

from collections.abc import Iterator

from actions.base import Action, EntityAction
from component.item import Item
from component.location import Location


class PickupItem(EntityAction):
    def poll(self) -> PickupItem | None:
        if "IsItem" not in self.target.tags:
            return None
        return self

    def action(self) -> int | None:
        del self.target.components[Location]
        self.target.relation_tag["IsIn"] = self.entity
        self.report("{You} pick up the {item}.", item=self.target.components[Item].name)
        return 100


class PickupGeneral(Action):
    def get_items(self) -> Iterator[PickupItem]:
        loc = self.entity.components[Location]
        for target in self.entity.world.Q.all_of(tags=[loc, "IsItem"]):
            action = PickupItem(self.entity, target).poll()
            if action:
                yield action

    def poll(self) -> Action | None:
        actions = list(self.get_items())
        if actions:
            return actions[0]
        return None
