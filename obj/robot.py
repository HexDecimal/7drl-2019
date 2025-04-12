from __future__ import annotations

from typing import TYPE_CHECKING

import tcod.ecs

import component.actor
import game.actions
from component.location import Location
from game.components import Graphic, Interactable, Name
from game.tags import IsBlocking
from game.verbs import take_control_interaction

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
            Graphic: Graphic(ch=ord("R")),
            Interactable: take_control_interaction,
            component.actor.Actor: RobotActor(),
        },
    )
    new_entity.components[Name] = "robot"
    new_entity.tags.add(IsBlocking)
    return new_entity
