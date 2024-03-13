"""Common helper functions for world interaction."""

from __future__ import annotations

import tcod.ecs

import engine.zone
import g


def active_zone() -> engine.zone.Zone:
    """Return the active zone."""
    return g.world[None].components[engine.zone.Zone]


def active_player() -> tcod.ecs.Entity:
    """The primary player entity."""
    return g.world[None].components[("player", tcod.ecs.Entity)]


def get_controlled_actor() -> tcod.ecs.Entity:
    """The active player controlled entity."""
    player = active_zone().player
    assert player is not None
    return player
