from __future__ import annotations

from typing import TYPE_CHECKING

import tcod.ecs

import component.actor
import component.graphic
import component.physicality
import component.verb
import game.actions
from component.location import Location

if TYPE_CHECKING:
    from game.action import Action


class RobotActor(component.actor.Actor):
    @classmethod
    def act(cls, entity: tcod.ecs.Entity) -> Action:  # noqa: ARG003
        return game.actions.Standby()


def new_robot(world: tcod.ecs.World, location: Location) -> tcod.ecs.Entity:
    new_entity = world[object()]
    new_entity.components.update(
        {
            Location: location,
            component.physicality.Physicality: component.physicality.Physicality(name="robot"),
            component.graphic.Graphic: component.graphic.Graphic(ch=ord("R")),
            component.verb.Interactable: component.verb.TakeControlInteractable(),
            component.actor.Actor: RobotActor(),
        },
    )
    return new_entity
