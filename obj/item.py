from __future__ import annotations

import tcod.ecs

from component.location import Location
from game.components import Graphic, Name
from game.tags import IsItem


def new_item(world: tcod.ecs.Registry, location: Location) -> tcod.ecs.Entity:
    new_entity = world[object()]
    new_entity.components.update(
        {
            Location: location,
            Graphic: Graphic(ch=ord("!"), priority=-1),
        },
    )
    new_entity.tags |= {IsItem}
    return new_entity


def new_spare_core(world: tcod.ecs.Registry, location: Location) -> tcod.ecs.Entity:
    new_entity = new_item(world, location)
    new_entity.components.update(
        {
            Graphic: Graphic(ch=ord("°"), priority=-1),
        },
    )
    new_entity.components[Name] = "spare drive core"
    new_entity.tags |= {"drive core"}
    return new_entity
