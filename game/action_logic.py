"""Action handling logic."""

from __future__ import annotations

import tcod.ecs

import component.actor
from game.action import Action, Success


def do_action(actor: tcod.ecs.Entity, action: Action) -> bool:
    """Attempt the action and return True if the action was performed."""
    # Ensure this actor was not already scheduled.
    assert actor.components[component.actor.Actor].ticket is None, "Actor is already waiting after an action."
    match action.__call__(actor):
        case Success(time_cost=time_cost):
            actor.components[component.actor.Actor].schedule(actor, time_cost)
    return True


def report(obj: tcod.ecs.Entity, string: str, **fmt: object) -> None:
    substitutions = {
        "you": "you",
        "You": "You",
    }
    obj.registry[None].components[("log", list[str])].append(string.format(**substitutions, **fmt))
