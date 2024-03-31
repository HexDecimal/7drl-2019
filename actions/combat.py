from __future__ import annotations

import attrs
import tcod.ecs

import actions.base
import actions.movement
import component.actor
import component.graphic
from actions import ActionResult, Impossible, Success
from component.location import Location
from component.physicality import Physicality


@attrs.define()
class Attack:
    target: tcod.ecs.Entity

    def perform(self, entity: tcod.ecs.Entity) -> ActionResult:
        if Physicality not in entity.components:
            return Impossible("")
        if Physicality not in self.target.components:
            return Impossible("")
        if not entity.components[Location].is_adjacent(self.target.components[Location]):
            return Impossible("")

        del self.target.components[component.actor.Actor]
        self.target.components[component.graphic.Graphic] = component.graphic.Graphic(ord("%"), (63, 63, 63))
        return Success(entity.components[Physicality].attack_speed)


@attrs.define()
class BumpAttack(actions.base.BumpAction):
    def perform(self, entity: tcod.ecs.Entity) -> ActionResult:
        destination = entity.components[Location] + self.direction
        for target in entity.world.Q.all_of(tags=[destination], components=[component.actor.Actor]):
            return Attack(target).perform(entity)
        return Impossible("Nothing to attack.")
