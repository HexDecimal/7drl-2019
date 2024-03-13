"""State logic functions."""

from __future__ import annotations

import tcod.event

import g
from game.state import Pop, Push, Rebase, StateResult


def handle_result(result: StateResult) -> None:
    """Apply a StateResult to the stack."""
    match result:
        case Push(state=new_state):
            g.states.append(new_state)
            new_state.on_enter()
        case Pop():
            g.states[-1].on_exit()
            g.states.pop()
        case Rebase(state=new_state):
            while g.states:
                handle_result(Pop())
            handle_result(Push(new_state))
        case None:
            pass


def loop() -> None:
    """State based game loop."""
    while g.states:
        g.states[-1].on_draw()
        for event in tcod.event.wait():
            if g.states:
                g.states[-1].on_event(event)
