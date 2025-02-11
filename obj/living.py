from __future__ import annotations

import tcod.ecs

import component.actor
import component.graphic
import component.physicality
import component.verb
from component.location import Location


def new_human(world: tcod.ecs.World, location: Location) -> tcod.ecs.Entity:
    new_entity = world[object()]
    new_entity.components.update(
        {
            Location: location,
            component.physicality.Physicality: component.physicality.Physicality(name="human"),
            component.graphic.Graphic: component.graphic.Graphic(ch=ord("U")),
            component.actor.Actor: component.actor.Actor(),
        },
    )
    return new_entity


def new_player(world: tcod.ecs.World, location: Location) -> tcod.ecs.Entity:
    new_entity = new_human(world, location)
    new_entity.components.update(
        {
            Location: location,
            component.physicality.Physicality: component.physicality.Physicality(name="you"),
            component.graphic.Graphic: component.graphic.Graphic(ch=ord("@")),
            component.verb.Interactable: component.verb.TakeControlInteractable(),
            component.actor.Actor: component.actor.Actor(controlled=True),
        },
    )
    return new_entity
