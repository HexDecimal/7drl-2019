from __future__ import annotations

import tcod.ecs

from component.location import Location
from game.action import ActionResult, Success
from game.action_logic import report
from game.components import Graphic, Interactable
from game.tags import IsBlocking


def door_interaction(
    issuer: tcod.ecs.Entity,
    target: tcod.ecs.Entity,
) -> ActionResult:
    target.clear()
    report(issuer, "{You} open the door.")
    return Success()


def new_auto_door(world: tcod.ecs.Registry, location: Location) -> tcod.ecs.Entity:
    new_entity = world[object()]
    new_entity.components.update(
        {
            Location: location,
            Graphic: Graphic(ch=ord("+")),
            Interactable: door_interaction,
        },
    )
    new_entity.tags.add(IsBlocking)
    return new_entity
