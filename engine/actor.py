from typing import Any, Optional

import tqueue

import engine.component
import engine.entity


class Actor(engine.component.Component):
    ticket: Optional[tqueue.Ticket] = None

    def on_added(self, entity: "engine.entity.Entity") -> None:
        self.entity: Optional[engine.entity.Entity] = entity
        self.schedule(0)

    def on_remove(self, entity: "engine.entity.Entity") -> None:
        self.entity = None
        self.ticket = None

    def schedule(self, interval: int) -> None:
        assert self.entity
        self.ticket = self.entity.location.world.tqueue.schedule(0, self)

    def act(self) -> None:
        self.schedule(100)

    def __call__(self) -> None:
        self.act()


class Player(Actor):

    def act(self) -> None:
        assert self.entity
        self.entity.location.world.player = self.entity
