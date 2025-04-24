"""Action handling logic."""

from __future__ import annotations

import tcod.ecs

import component.actor
import engine.helpers
from game.action import Action, Success
from game.components import MessageLog
from game.tags import IsControlled
from game.typing import Ticket_, TurnQueue_


def do_action(actor: tcod.ecs.Entity, action: Action) -> bool:
    """Attempt the action and return True if the action was performed."""
    # Ensure this actor was not already scheduled.
    assert Ticket_ not in actor.components, "Actor is already waiting after an action."
    match action.__call__(actor):
        case Success(time_cost=time_cost):
            actor.components[component.actor.Actor].schedule(actor, time_cost)
    return True


def simulate(world: tcod.ecs.Registry) -> None:
    """Run world simulation until it is the players turn."""
    while not world.Q.all_of(tags=[IsControlled]):
        ticket = world[None].components[TurnQueue_].pop()
        component.actor.Actor.call(ticket, ticket.value)
        if component.actor.Actor not in engine.helpers.active_player().components:
            msg = "Player has died."
            raise SystemExit(msg)
    for entity in world.Q.all_of(tags=[IsControlled]):
        entity.components.pop(Action, None)  # Clear PlayerControl action.


def report(obj: tcod.ecs.Entity, string: str, **fmt: object) -> None:
    substitutions = {
        "you": "you",
        "You": "You",
    }
    obj.registry[None].components[MessageLog].append(string.format(**substitutions, **fmt))
