from typing import Optional, TYPE_CHECKING

import tqueue

import actions
import engine.component
if TYPE_CHECKING:
    import engine.entity


class Actor(engine.component.Component):
    ticket: Optional[tqueue.Ticket] = None

    def on_added(self, entity: "engine.entity.Entity") -> None:
        self.entity: Optional[engine.entity.Entity] = entity
        self.schedule(0)

    def on_remove(self, entity: "engine.entity.Entity") -> None:
        self.entity = None
        self.ticket = None

    def on_destroy(self, entity: "engine.entity.Entity") -> None:
        assert self.entity
        entity.actor = None

    def schedule(self, interval: int) -> None:
        assert self.entity
        self.ticket = self.world.tqueue.schedule(interval, self)
        if self.world.player is self.entity:
            self.world.player = None

    def act(self) -> None:
        assert self.entity
        actions.Wait(self.entity).invoke()

    def __call__(self, ticket: tqueue.Ticket) -> None:
        if self.ticket is ticket:
            self.ticket = None
            self.act()
            assert self.ticket or self.is_player_controlled()

    def is_player_controlled(self) -> bool:
        return False


class Player(Actor):

    def act(self) -> None:
        assert self.entity
        self.ticket = None
        self.world.player = self.entity

    def is_player_controlled(self) -> bool:
        return True
