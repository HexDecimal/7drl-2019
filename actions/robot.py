from __future__ import annotations

import attrs
import tcod.ecs

import component.actor
from actions import ActionResult, Impossible, Success
from engine.helpers import active_player
from game.actions import report


@attrs.define()
class ReturnControlToPlayer:
    def perform(self, entity: tcod.ecs.Entity) -> ActionResult:
        player = active_player()
        if entity is player:
            return Impossible("Already player.")
        entity.components[component.actor.Actor].controlled = False
        component.actor.Actor.take_control(player)
        report(entity, "{You} stop controlling the robot.")
        return Success(time_cost=0)


@attrs.define()
class RemoteControl:
    target: tcod.ecs.Entity

    def perform(self, entity: tcod.ecs.Entity) -> ActionResult:
        if self.target is active_player():
            return ReturnControlToPlayer().perform(entity)
        entity.components[component.actor.Actor].controlled = False
        component.actor.Actor.take_control(self.target)
        report(entity, "{You} begin controlling the robot remotely.")
        return Success(time_cost=0)
