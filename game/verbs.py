"""Common entity interactions."""

from __future__ import annotations

from typing import TYPE_CHECKING

import tcod.ecs

import game.actions

if TYPE_CHECKING:
    from game.action import ActionResult


def take_control_interaction(issuer: tcod.ecs.Entity, target: tcod.ecs.Entity) -> ActionResult:
    """Allow taking control of this entity."""
    return game.actions.RemoteControl(target).__call__(issuer)
