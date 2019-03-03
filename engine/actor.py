from typing import Optional

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
        self.ticket = self.world.tqueue.schedule(interval, self)
        if self.world.player is self.entity:
            self.world.player = None

    def act(self) -> None:
        self.schedule(100)

    def __call__(self, ticket: tqueue.Ticket) -> None:
        if self.ticket is ticket:
            self.act()
            assert self.ticket is not ticket


class Player(Actor):

    def act(self) -> None:
        assert self.entity
        self.ticket = None
        self.world.player = self.entity
