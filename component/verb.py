from __future__ import annotations

import attrs
import tcod.ecs

import game.action
import game.actions
from game.action import ActionResult, Impossible


class Interactable:
    def interaction(self, issuer: tcod.ecs.Entity, target: tcod.ecs.Entity) -> ActionResult:
        return Impossible("No interaction.")


class TakeControlInteractable(Interactable):
    def interaction(self, issuer: tcod.ecs.Entity, target: tcod.ecs.Entity) -> ActionResult:
        return game.actions.RemoteControl(target).__call__(issuer)


class Interaction(Interactable):
    @attrs.define()
    class Action(game.action.Action):
        target: tcod.ecs.Entity

        def __call__(self, entity: tcod.ecs.Entity) -> ActionResult:
            return Impossible("No interaction.")

    def interaction(self, issuer: tcod.ecs.Entity, target: tcod.ecs.Entity) -> ActionResult:
        return self.Action(target).__call__(issuer)
