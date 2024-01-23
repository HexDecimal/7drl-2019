from __future__ import annotations

import tcod.ecs

import component.graphic
import component.item
from component.location import Location


def new_item(world: tcod.ecs.World, location: Location) -> tcod.ecs.Entity:
    new_entity = world[object()]
    new_entity.components.update(
        {
            Location: location,
            component.graphic.Graphic: component.graphic.Graphic(ch=ord("!"), priority=-1),
            component.item.Item: component.item.Item(),
        }
    )
    new_entity.tags |= {"IsItem"}
    return new_entity


def new_spare_core(world: tcod.ecs.World, location: Location) -> tcod.ecs.Entity:
    new_entity = new_item(world, location)
    new_entity.components.update(
        {
            component.graphic.Graphic: component.graphic.Graphic(ch=ord("°"), priority=-1),
            component.item.Item: component.item.Item(name="spare drive core", tags=frozenset({"drive core"})),
        }
    )
    new_entity.tags |= {"drive core"}
    return new_entity
