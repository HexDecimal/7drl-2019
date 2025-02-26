from __future__ import annotations

from typing import TYPE_CHECKING

import attrs
import tcod.ecs
import tcod.ecs.callbacks

import game.actions
from engine.helpers import active_zone
from game.action import Action
from tqueue.tqueue import Ticket

if TYPE_CHECKING:
    import tqueue.tqueue


@attrs.define(kw_only=True)
class Actor:
    controlled: bool = False

    @staticmethod
    def schedule(entity: tcod.ecs.Entity, interval: int) -> None:
        """Schedule an entity at interval."""
        assert Ticket not in entity.components
        entity.components[Ticket] = active_zone().tqueue.schedule(interval, entity)
        if active_zone().player is entity:
            active_zone().player = None

    @classmethod
    def act(cls, entity: tcod.ecs.Entity) -> Action:  # noqa: ARG003
        return game.actions.wait

    @classmethod
    def call(cls, ticket: tqueue.tqueue.Ticket[tcod.ecs.Entity], entity: tcod.ecs.Entity) -> None:
        self = entity.components[Actor]
        if entity.components.get(Ticket) is ticket:
            del entity.components[Ticket]
            entity.components.pop(Action, None)
            if not self.controlled:
                entity.components[Action] = cls.act(entity)
                if not entity.components[Action].__call__(entity):
                    self.schedule(entity, 100)
            else:
                game.actions.PlayerControl().__call__(entity)

    def is_controlled(self) -> bool:
        return self.controlled

    @staticmethod
    def take_control(entity: tcod.ecs.Entity) -> None:
        self = entity.components[Actor]
        self.interrupt(entity, force=True)
        game.actions.PlayerControl().__call__(entity)

    @staticmethod
    def interrupt(entity: tcod.ecs.Entity, *, force: bool = False) -> None:  # noqa: ARG004
        entity.components.pop(Ticket, None)
        entity.components.pop(Action, None)


@tcod.ecs.callbacks.register_component_changed(component=Actor)
def on_actor_changed(entity: tcod.ecs.Entity, old: Actor | None, new: Actor | None) -> None:
    """Handle scheduling on Actor components being added and removed."""
    if old == new:
        return
    if old is not None:
        entity.components.pop(Ticket, None)
    if new is not None:
        Actor.schedule(entity, 0)
