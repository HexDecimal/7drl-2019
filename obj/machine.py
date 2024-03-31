from __future__ import annotations

import attrs
import tcod.ecs

import component.graphic
import component.physicality
import component.verb
from actions import ActionResult, Impossible, Success
from component.location import Location
from game.actions import report


def new_machine(world: tcod.ecs.World, location: Location) -> tcod.ecs.Entity:
    new_entity = world[object()]
    new_entity.components.update(
        {
            Location: location,
            component.physicality.Physicality: component.physicality.Physicality(),
            component.graphic.Graphic: component.graphic.Graphic(ch=ord("#")),
        }
    )
    return new_entity


class DriveCoreInteractable(component.verb.Interaction):
    @attrs.define()
    class Action:
        target: tcod.ecs.Entity

        def get_core(self, entity: tcod.ecs.Entity) -> tcod.ecs.Entity | None:
            for item in entity.world.Q.all_of(tags=["drive core"], relations=[("IsIn", entity)]):
                return item
            return None

        def perform(self, entity: tcod.ecs.Entity) -> ActionResult:
            if not self.get_core(entity):
                return Impossible("Need core.")

            core = self.get_core(entity)
            assert core
            core.relation_tag["IsIn"] = self.target
            report(entity, "{You} install the core.")
            return Success()


def new_drive_core(world: tcod.ecs.World, location: Location) -> tcod.ecs.Entity:
    new_entity = new_machine(world, location)
    new_entity.components.update(
        {
            component.graphic.Graphic: component.graphic.Graphic(ch=ord("╪")),
            component.verb.Interactable: DriveCoreInteractable(),
        }
    )
    return new_entity
