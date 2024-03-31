from __future__ import annotations

from collections.abc import Iterator

import attrs
import tcod.ecs

from actions import ActionResult, Impossible, Success
from component.item import Item
from component.location import Location
from game.actions import report


@attrs.define()
class PickupItem:
    target: tcod.ecs.Entity

    def perform(self, entity: tcod.ecs.Entity) -> ActionResult:
        if "IsItem" not in self.target.tags:
            return Impossible("Not an item.")

        del self.target.components[Location]
        self.target.relation_tag["IsIn"] = entity
        report(entity, "{You} pick up the {item}.", item=self.target.components[Item].name)
        return Success()


@attrs.define()
class PickupGeneral:
    def get_items(self, entity: tcod.ecs.Entity) -> Iterator[ActionResult]:
        loc = entity.components[Location]
        for target in entity.world.Q.all_of(tags=[loc, "IsItem"]):
            action = PickupItem(target).perform(entity)
            if action:
                yield action

    def perform(self, entity: tcod.ecs.Entity) -> ActionResult:
        actions = list(self.get_items(entity))
        if actions:
            return actions[0]
        return Impossible("No items on floor.")
