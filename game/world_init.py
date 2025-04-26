"""World initialization."""

from __future__ import annotations

from random import Random

import tcod.ecs

import obj.living
import procgen.shipgen
from component.location import Location
from game.components import Graphic, MessageLog, Name
from game.tags import IsIn, IsItem, IsStartPos
from game.typing import TurnQueue_


def init_world(world: tcod.ecs.Registry) -> None:
    """Initialize or reinitialize a world."""
    base_item = world["item"]
    base_item.components[Graphic] = Graphic(ch=ord("!"), priority=-1)
    base_item.tags |= {IsItem}

    spare_core = world["spare core"]
    spare_core.relation_tag[tcod.ecs.IsA] = base_item
    spare_core.components[Graphic] = Graphic(ch=ord("°"), priority=-1)
    spare_core.components[Name] = "spare drive core"
    spare_core.tags |= {"drive core"}


def new_world() -> tcod.ecs.Registry:
    """Return a new world."""
    world = tcod.ecs.Registry()
    world[None].components[Random] = Random(1)
    world[None].components[MessageLog] = []
    world[None].components[TurnQueue_] = TurnQueue_()

    init_world(world)

    ship = procgen.shipgen.Ship().generate(world)

    (start_pos,) = world.Q.all_of(tags=[IsStartPos], relations=[(IsIn, ship)])
    obj.living.new_player(world, start_pos.components[Location])

    return world
