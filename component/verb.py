from __future__ import annotations

import attrs
import tcod.ecs

import actions.base
import actions.robot
from actions import ActionResult, Impossible


class Interactable:
    def interaction(self, issuer: tcod.ecs.Entity, target: tcod.ecs.Entity) -> ActionResult:
        return Impossible("No interaction.")


class TakeControlInteractable(Interactable):
    def interaction(self, issuer: tcod.ecs.Entity, target: tcod.ecs.Entity) -> ActionResult:
        return actions.robot.RemoteControl(target).perform(issuer)


class Interaction(Interactable):
    @attrs.define()
    class Action(actions.Action):
        target: tcod.ecs.Entity

        def perform(self, entity: tcod.ecs.Entity) -> ActionResult:
            return Impossible("No interaction.")

    def interaction(self, issuer: tcod.ecs.Entity, target: tcod.ecs.Entity) -> ActionResult:
        return self.Action(target).perform(issuer)
