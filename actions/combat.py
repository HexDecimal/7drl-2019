from __future__ import annotations

from typing import Optional

import actions.base
import actions.movement
import component.graphic


class Attack(actions.base.EntityAction):
    def poll(self) -> Optional[Attack]:
        if not self.entity.character:
            return None
        if not self.target.character:
            return None
        if not self.entity.location.is_adjacent(self.target.location):
            return None
        return self

    def action(self) -> int:
        assert self.entity.character
        assert self.target.character
        self.target.actor = None
        self.target.graphic = component.graphic.Graphic(ord('%'), (63, 63, 63))
        return self.entity.character.attack_speed


class BumpAttack(actions.base.BumpAction):
    def poll(self) -> Optional[actions.base.Action]:
        for target in self.destination.contents:
            if target.actor:
                return Attack(self.entity, target).poll()
        return None
