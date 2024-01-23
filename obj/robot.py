from __future__ import annotations

import tcod.ecs

import actions.base
import actions.common
import component.actor
import component.graphic
import component.physicality
import component.verb
from component.location import Location


class RobotActor(component.actor.Actor):
    @classmethod
    def act(cls, entity: tcod.ecs.Entity) -> actions.base.Action:
        return actions.common.Standby(entity)


def new_robot(world: tcod.ecs.World, location: Location) -> tcod.ecs.Entity:
    new_entity = world[object()]
    new_entity.components.update(
        {
            Location: location,
            component.physicality.Physicality: component.physicality.Physicality(name="robot"),
            component.graphic.Graphic: component.graphic.Graphic(ch=ord("R")),
            component.verb.Interactable: component.verb.TakeControlInteractable(),
            component.actor.Actor: RobotActor(),
        }
    )
    return new_entity
