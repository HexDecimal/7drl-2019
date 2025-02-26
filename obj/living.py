from __future__ import annotations

import tcod.ecs

import component.actor
import component.graphic
from component.location import Location
from game.components import Interactable, Name
from game.tags import IsBlocking, IsControllable
from game.verbs import take_control_interaction


def new_human(world: tcod.ecs.World, location: Location) -> tcod.ecs.Entity:
    new_entity = world[object()]
    new_entity.components.update(
        {
            Location: location,
            component.graphic.Graphic: component.graphic.Graphic(ch=ord("U")),
            component.actor.Actor: component.actor.Actor(),
        },
    )
    new_entity.components[Name] = "human"
    new_entity.tags.add(IsBlocking)
    return new_entity


def new_player(world: tcod.ecs.World, location: Location) -> tcod.ecs.Entity:
    new_entity = new_human(world, location)
    new_entity.components.update(
        {
            Location: location,
            component.graphic.Graphic: component.graphic.Graphic(ch=ord("@")),
            Interactable: take_control_interaction,
            component.actor.Actor: component.actor.Actor(),
        },
    )
    new_entity.components[Name] = "you"
    new_entity.tags.add(IsBlocking)
    new_entity.tags.add(IsControllable)
    return new_entity
