from __future__ import annotations

import tcod.ecs

import engine.zone
import g
import procgen.shipgen
from game.components import MessageLog
from game.typing import TurnQueue_


def init() -> None:
    """Initialize the world globally."""
    g.world = tcod.ecs.Registry()
    g.world[None].components[MessageLog] = []
    g.world[None].components[TurnQueue_] = TurnQueue_()

    ship = procgen.shipgen.Ship(1)
    g.world[None].components[engine.zone.Zone] = ship.zone
    g.world[None].components[("player", tcod.ecs.Entity)] = ship.player
