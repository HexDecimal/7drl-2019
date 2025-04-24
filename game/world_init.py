"""World initialization."""

from __future__ import annotations

import tcod.ecs

import engine.zone
import procgen.shipgen
from game.components import MessageLog
from game.typing import TurnQueue_


def new_world() -> tcod.ecs.Registry:
    """Return a new world."""
    world = tcod.ecs.Registry()
    world[None].components[MessageLog] = []
    world[None].components[TurnQueue_] = TurnQueue_()

    ship = procgen.shipgen.Ship(world, 1)
    world[None].components[engine.zone.Zone] = ship.zone
    world[None].components[("player", tcod.ecs.Entity)] = ship.player

    return world
