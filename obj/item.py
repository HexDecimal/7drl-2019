from __future__ import annotations

import tcod.ecs

from component.location import Location


def new_item(world: tcod.ecs.Registry, location: Location) -> tcod.ecs.Entity:
    new_entity = world["item"].instantiate()
    new_entity.components[Location] = location
    return new_entity


def new_spare_core(world: tcod.ecs.Registry, location: Location) -> tcod.ecs.Entity:
    new_entity = world["spare core"].instantiate()
    new_entity.components[Location] = location
    return new_entity
