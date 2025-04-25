from __future__ import annotations

import tcod.ecs

import component.actor
from component.location import Location
from game.components import Graphic, Interactable, Name
from game.tags import IsBlocking, IsControllable, IsPlayer
from game.verbs import take_control_interaction


def new_human(world: tcod.ecs.Registry, location: Location) -> tcod.ecs.Entity:
    new_entity = world[object()]
    new_entity.components.update(
        {
            Location: location,
            Graphic: Graphic(ch=ord("U")),
            component.actor.Actor: component.actor.Actor(),
        },
    )
    new_entity.components[Name] = "human"
    new_entity.tags.add(IsBlocking)
    return new_entity


def new_player(world: tcod.ecs.Registry, location: Location) -> tcod.ecs.Entity:
    new_entity = new_human(world, location)
    new_entity.components.update(
        {
            Location: location,
            Graphic: Graphic(ch=ord("@")),
            Interactable: take_control_interaction,
            component.actor.Actor: component.actor.Actor(),
        },
    )
    new_entity.components[Name] = "you"
    new_entity.tags.add(IsBlocking)
    new_entity.tags.add(IsControllable)
    new_entity.tags.add(IsPlayer)
    return new_entity
