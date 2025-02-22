from __future__ import annotations

import tcod.ecs

import engine.zone
import g
import procgen.shipgen
from game.components import MessageLog


def init() -> None:
    g.world = tcod.ecs.World()
    g.world[None].components[MessageLog] = []

    ship = procgen.shipgen.Ship(1)
    g.world[None].components[engine.zone.Zone] = ship.zone
    g.world[None].components[("player", tcod.ecs.Entity)] = ship.player
