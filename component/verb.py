from __future__ import annotations

import tcod.ecs

import actions.base
import actions.robot


class Interactable:
    def interaction(self, issuer: tcod.ecs.Entity, target: tcod.ecs.Entity) -> actions.base.Action | None:
        return None


class TakeControlInteractable(Interactable):
    def interaction(self, issuer: tcod.ecs.Entity, target: tcod.ecs.Entity) -> actions.base.Action | None:
        return actions.robot.RemoteControl(issuer, target).poll()


class Interaction(Interactable):
    class Action(actions.base.EntityAction):
        pass

    def interaction(self, issuer: tcod.ecs.Entity, target: tcod.ecs.Entity) -> actions.base.Action | None:
        return self.Action(issuer, target).poll()
