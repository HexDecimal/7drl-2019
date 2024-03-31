from __future__ import annotations

import tcod.ecs

import component.graphic
import component.physicality
import component.verb
from actions import ActionResult, Success
from component.location import Location
from game.actions import report


class DoorInteractable(component.verb.Interactable):
    def interaction(
        self,
        issuer: tcod.ecs.Entity,
        target: tcod.ecs.Entity,
    ) -> ActionResult:
        del target.components[component.graphic.Graphic]
        target.components[component.physicality.Physicality].blocking = False
        report(issuer, "{You} open the door.")
        return Success()


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
