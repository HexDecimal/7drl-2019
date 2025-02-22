from __future__ import annotations

import tcod.ecs

import component.graphic
import component.verb
from component.location import Location
from game.action import ActionResult, Success
from game.action_logic import report
from game.tags import IsBlocking


class DoorInteractable(component.verb.Interactable):
    def interaction(
        self,
        issuer: tcod.ecs.Entity,
        target: tcod.ecs.Entity,
    ) -> ActionResult:
        target.clear()
        report(issuer, "{You} open the door.")
        return Success()


def new_auto_door(world: tcod.ecs.World, location: Location) -> tcod.ecs.Entity:
    new_entity = world[object()]
    new_entity.components.update(
        {
            Location: location,
            component.graphic.Graphic: component.graphic.Graphic(ch=ord("+")),
            component.verb.Interactable: DoorInteractable(),
        },
    )
    new_entity.tags.add(IsBlocking)
    return new_entity
