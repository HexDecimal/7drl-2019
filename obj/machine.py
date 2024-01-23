from __future__ import annotations

import tcod.ecs

import actions.base
import component.graphic
import component.physicality
import component.verb
from component.location import Location


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
    class Action(actions.base.EntityAction):
        def get_core(self) -> tcod.ecs.Entity | None:
            for item in self.entity.world.Q.all_of(tags=["drive core"], relations=[("IsIn", self.entity)]):
                return item
            return None

        def poll(self) -> actions.base.Action | None:
            if self.get_core():
                return self
            return None

        def action(self) -> int:
            core = self.get_core()
            assert core
            core.relation_tag["IsIn"] = self.target
            self.report("{You} install the core.")
            return 100


def new_drive_core(world: tcod.ecs.World, location: Location) -> tcod.ecs.Entity:
    new_entity = new_machine(world, location)
    new_entity.components.update(
        {
            component.graphic.Graphic: component.graphic.Graphic(ch=ord("╪")),
            component.verb.Interactable: DriveCoreInteractable(),
        }
    )
    return new_entity
