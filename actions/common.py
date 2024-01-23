from __future__ import annotations

import tcod.ecs

import actions.base
import actions.combat
import actions.movement
import component.actor
from component.location import Location
from component.verb import Interactable


class Wait(actions.base.Action):
    def action(self) -> int:
        return 100


class Interact(actions.base.EntityAction):
    def poll(self) -> actions.base.Action | None:
        if Interactable in self.target.components:
            return self.target.components[Interactable].interaction(self.entity, self.target)
        return None


class BumpInteract(actions.base.BumpAction):
    def poll(self) -> actions.base.Action | None:
        for target in self.entity.world.Q.all_of(tags=[self.destination], components=[Interactable]):
            return Interact(self.entity, target).poll()
        return None


class Bump(actions.base.Action):
    def __init__(
        self,
        entity: tcod.ecs.Entity,
        direction: tuple[int, int, int],
    ) -> None:
        super().__init__(entity)
        self.direction = direction

    ACTIONS = (
        actions.movement.MoveBy,
        BumpInteract,
        actions.combat.BumpAttack,
    )

    def poll(self) -> actions.base.Action | None:
        for action_type in self.ACTIONS:
            action = action_type(self.entity, self.direction).poll()
            if action is not None:
                return action
        return None


class PlayerControl(actions.base.Action):
    """Give immediate user control to this entity."""

    def action(self) -> int | None:
        self.entity.components[component.actor.Actor].controlled = True
        self.entity.components[Location].zone.camera = self.entity.components[Location].xyz
        self.entity.components[Location].zone.player = self.entity
        return None  # Further actions will be pending.


class Standby(actions.base.Action):
    def action(self) -> None:
        return None
