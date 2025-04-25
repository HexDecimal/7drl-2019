"""World initialization."""

from __future__ import annotations

import tcod.ecs

import obj.living
import procgen.shipgen
from component.location import Location
from game.components import MessageLog
from game.tags import IsStartPos
from game.typing import TurnQueue_


def new_world() -> tcod.ecs.Registry:
    """Return a new world."""
    world = tcod.ecs.Registry()
    world[None].components[MessageLog] = []
    world[None].components[TurnQueue_] = TurnQueue_()

    ship = procgen.shipgen.Ship(world, 1)

    (start_pos,) = world.Q.all_of(tags=[IsStartPos])
    obj.living.new_player(world, start_pos.components[Location])

    return world
