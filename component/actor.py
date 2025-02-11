from __future__ import annotations

from typing import TYPE_CHECKING

import attrs
import tcod.ecs
import tcod.ecs.callbacks

import game.actions
from engine.helpers import active_zone

if TYPE_CHECKING:
    import tqueue.tqueue
    from game.action import Action


@attrs.define(kw_only=True)
class Actor:
    controlled: bool = False
    ticket: tqueue.tqueue.Ticket[tcod.ecs.Entity] | None = None
    action: Action | None = None

    @staticmethod
    def schedule(entity: tcod.ecs.Entity, interval: int) -> None:
        self = entity.components[Actor]
        assert self.ticket is None
        self.ticket = active_zone().tqueue.schedule(interval, entity)
        if active_zone().player is entity:
            active_zone().player = None

    @classmethod
    def act(cls, entity: tcod.ecs.Entity) -> Action:  # noqa: ARG003
        return game.actions.wait

    @classmethod
    def call(cls, ticket: tqueue.tqueue.Ticket[tcod.ecs.Entity], entity: tcod.ecs.Entity) -> None:
        self = entity.components[Actor]
        if self.ticket is ticket:
            self.ticket = None
            self.action = None
            if not self.controlled:
                self.action = cls.act(entity)
                if not self.action.__call__(entity):
                    self.schedule(entity, 100)
            else:
                game.actions.PlayerControl().__call__(entity)

    def is_controlled(self) -> bool:
        return self.controlled

    @staticmethod
    def take_control(entity: tcod.ecs.Entity) -> None:
        self = entity.components[Actor]
        self.interrupt(force=True)
        game.actions.PlayerControl().__call__(entity)

    def interrupt(self, *, force: bool = False) -> None:  # noqa: ARG002
        self.ticket = None
        self.action = None


@tcod.ecs.callbacks.register_component_changed(component=Actor)
def on_actor_changed(entity: tcod.ecs.Entity, old: Actor | None, new: Actor | None) -> None:
    """Handle scheduling on Actor components being added and removed."""
    if old == new:
        return
    if old is not None:
        entity.components[Actor].ticket = None
    if new is not None:
        Actor.schedule(entity, 0)
