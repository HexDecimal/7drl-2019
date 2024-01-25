from __future__ import annotations

import attrs
import tcod.ecs
import tcod.ecs.callbacks

import actions.base
import actions.common
import tqueue.tqueue
from engine.helpers import active_zone


@attrs.define(kw_only=True)
class Actor:
    controlled: bool = False
    ticket: tqueue.tqueue.Ticket[tcod.ecs.Entity] | None = None
    action: actions.base.Action | None = None

    @staticmethod
    def schedule(entity: tcod.ecs.Entity, interval: int) -> None:
        self = entity.components[Actor]
        assert self.ticket is None
        self.ticket = active_zone().tqueue.schedule(interval, entity)
        if active_zone().player is entity:
            active_zone().player = None

    @classmethod
    def act(cls, entity: tcod.ecs.Entity) -> actions.base.Action:
        return actions.common.Wait(entity)

    @classmethod
    def call(cls, ticket: tqueue.tqueue.Ticket[tcod.ecs.Entity], entity: tcod.ecs.Entity) -> None:
        self = entity.components[Actor]
        if self.ticket is ticket:
            self.ticket = None
            self.action = None
            if not self.controlled:
                self.action = cls.act(entity)
                if not self.action.invoke():
                    self.schedule(entity, 100)
            else:
                actions.common.PlayerControl(entity).invoke()

    def is_controlled(self) -> bool:
        return self.controlled

    @staticmethod
    def take_control(entity: tcod.ecs.Entity) -> None:
        self = entity.components[Actor]
        self.interrupt(True)
        actions.common.PlayerControl(entity).invoke()

    def interrupt(self, force: bool = False) -> None:
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
