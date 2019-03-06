from __future__ import annotations

from typing import Iterator, Optional

from actions.base import Action, EntityAction


class PickupItem(EntityAction):
    def poll(self) -> Optional[PickupItem]:
        if not self.entity.container:
            return None
        if not self.target.item:
            return None
        return self

    def action(self) -> Optional[int]:
        assert self.entity.container
        self.target.location = self.entity.container
        return 100


class PickupGeneral(Action):
    def get_items(self) -> Iterator[PickupItem]:
        for target in self.entity.location.contents:
            if target is self.entity:
                continue
            action = PickupItem(self.entity, target).poll()
            if action:
                yield action

    def poll(self) -> Optional[Action]:
        actions = list(self.get_items())
        if actions:
            return actions[0]
        return None
