"""Base state types."""

from __future__ import annotations

from typing import Protocol, Union

import attrs
import tcod.console
import tcod.event


@attrs.define(frozen=True)
class Pop:
    """Remove the top state."""


@attrs.define(frozen=True)
class Push:
    """Push this state into the stack."""

    state: State


@attrs.define(frozen=True)
class Rebase:
    """Replace stack with a single state."""

    state: State


StateResult = Union[None, Push, Pop, Rebase]  # noqa: UP007


class State(Protocol):
    """Abstract state class."""

    __slots__ = ()

    def on_enter(self) -> None:
        """Called when a state is pushed."""
        return

    def on_exit(self) -> None:
        """Called when a state is popped."""
        return

    def on_draw(self, console: tcod.console.Console, /) -> None:
        """Called when a state is drawn."""
        ...

    def on_event(self, event: tcod.event.Event, /) -> StateResult:
        """Called when a state handles an event."""
        ...
