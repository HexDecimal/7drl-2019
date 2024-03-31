from __future__ import annotations

import attrs
import tcod.ecs

import actions.base
import actions.combat
import actions.movement
import component.actor
from actions import ActionResult, Impossible, Success
from component.location import Location
from component.verb import Interactable


class Wait:
    def perform(self, entity: tcod.ecs.Entity) -> ActionResult:
        return Success()


@attrs.define()
class Interact:
    target: tcod.ecs.Entity

    def perform(self, entity: tcod.ecs.Entity) -> ActionResult:
        if Interactable in self.target.components:
            return self.target.components[Interactable].interaction(entity, self.target)
        return Impossible("Not interactable.")


@attrs.define()
class BumpInteract(actions.base.BumpAction):
    def perform(self, entity: tcod.ecs.Entity) -> ActionResult:
        destination = entity.components[Location] + self.direction
        for target in entity.world.Q.all_of(tags=[destination], components=[Interactable]):
            return Interact(target).perform(entity)
        return Impossible("No target.")


@attrs.define()
class Bump:
    direction: tuple[int, int, int]

    def perform(self, entity: tcod.ecs.Entity) -> ActionResult:
        return (
            actions.movement.MoveBy(self.direction).perform(entity)
            or BumpInteract(self.direction).perform(entity)
            or actions.combat.BumpAttack(self.direction).perform(entity)
        )


@attrs.define()
class PlayerControl:
    """Give immediate user control to this entity."""

    def perform(self, entity: tcod.ecs.Entity) -> ActionResult:
        entity.components[component.actor.Actor].controlled = True
        entity.components[Location].zone.camera = entity.components[Location].xyz
        entity.components[Location].zone.player = entity
        return Impossible("End of action.")  # Further actions will be pending.


@attrs.define()
class Standby:
    def perform(self, entity: tcod.ecs.Entity) -> ActionResult:
        return Impossible("End of action.")
