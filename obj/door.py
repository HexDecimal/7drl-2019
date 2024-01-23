from __future__ import annotations

from typing import Self

import tcod.ecs

import actions.base
import component.graphic
import component.physicality
import component.verb
from component.location import Location


class DoorInteractable(component.verb.Interactable):
    class OpenDoor(actions.base.EntityAction):
        def poll(self) -> Self:
            return self

        def action(self) -> int:
            del self.target.components[component.graphic.Graphic]
            self.target.components[component.physicality.Physicality].blocking = False
            self.report("{You} open the door.")
            return 100

    def interaction(
        self,
        issuer: tcod.ecs.Entity,
        target: tcod.ecs.Entity,
    ) -> actions.base.Action | None:
        return self.OpenDoor(issuer, target)


def new_auto_door(world: tcod.ecs.World, location: Location) -> tcod.ecs.Entity:
    new_entity = world[object()]
    new_entity.components.update(
        {
            Location: location,
            component.physicality.Physicality: component.physicality.Physicality(),
            component.graphic.Graphic: component.graphic.Graphic(ch=ord("+")),
            component.verb.Interactable: DoorInteractable(),
        }
    )
    return new_entity
