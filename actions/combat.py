from __future__ import annotations

import actions.base
import actions.movement
import component.actor
import component.graphic
from component.location import Location
from component.physicality import Physicality


class Attack(actions.base.EntityAction):
    def poll(self) -> Attack | None:
        if Physicality not in self.entity.components:
            return None
        if Physicality not in self.target.components:
            return None
        if not self.entity.components[Location].is_adjacent(self.target.components[Location]):
            return None
        return self

    def action(self) -> int:
        del self.target.components[component.actor.Actor]
        self.target.components[component.graphic.Graphic] = component.graphic.Graphic(ord("%"), (63, 63, 63))
        return self.entity.components[Physicality].attack_speed


class BumpAttack(actions.base.BumpAction):
    def poll(self) -> actions.base.Action | None:
        for target in self.entity.world.Q.all_of(tags=[self.destination], components=[component.actor.Actor]):
            return Attack(self.entity, target).poll()
        return None
