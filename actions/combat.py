from __future__ import annotations

import actions.base
import actions.movement
import component.graphic


class Attack(actions.base.EntityAction):
    def poll(self) -> Attack | None:
        if not self.entity.physicality:
            return None
        if not self.target.physicality:
            return None
        if not self.entity.location.is_adjacent(self.target.location):
            return None
        return self

    def action(self) -> int:
        assert self.entity.physicality
        assert self.target.physicality
        self.target.actor = None
        self.target.graphic = component.graphic.Graphic(ord("%"), (63, 63, 63))
        return self.entity.physicality.attack_speed


class BumpAttack(actions.base.BumpAction):
    def poll(self) -> actions.base.Action | None:
        for target in self.destination.contents:
            if target.actor:
                return Attack(self.entity, target).poll()
        return None
