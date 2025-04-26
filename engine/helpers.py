"""Common helper functions for world interaction."""

from __future__ import annotations

import tcod.ecs

import g
from game.tags import IsControlled, IsIn, IsPlayer


def active_zone() -> tcod.ecs.Entity:
    """Return the active zone."""
    return g.world["camera"].relation_tag[IsIn]


def active_player() -> tcod.ecs.Entity:
    """The primary player entity."""
    (player,) = g.world.Q.all_of(tags=[IsPlayer])
    return player


def get_controlled_actor() -> tcod.ecs.Entity:
    """The active player controlled entity."""
    (player,) = g.world.Q.all_of(tags=[IsControlled])
    return player
