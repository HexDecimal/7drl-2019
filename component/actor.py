from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import actions.base
import actions.common
import component.base
import tqueue

if TYPE_CHECKING:
    import obj.entity


class Actor(component.base.OwnedComponent):
    controlled = False

    def __init__(self) -> None:
        super().__init__()
        self.ticket: Optional[tqueue.Ticket] = None
        self.action: Optional[actions.base.Action] = None

    def on_added(self, entity: obj.entity.Entity) -> None:
        super().on_added(entity)
        self.schedule(0)

    def on_remove(self, entity: obj.entity.Entity) -> None:
        super().on_remove(entity)
        self.ticket = None

    def on_destroy(self, entity: obj.entity.Entity) -> None:
        super().on_destroy(entity)
        self.owner.actor = None

    def schedule(self, interval: int) -> None:
        assert self.ticket is None
        self.ticket = self.zone.tqueue.schedule(interval, self)
        if self.zone.player is self.owner:
            self.zone.player = None

    def act(self) -> actions.base.Action:
        return actions.common.Wait(self.owner)

    def __call__(self, ticket: tqueue.Ticket) -> None:
        if self.ticket is ticket:
            self.ticket = None
            self.action = None
            if not self.controlled:
                self.action = self.act()
                if not self.action.invoke():
                    self.schedule(100)
            else:
                actions.common.PlayerControl(self.owner).invoke()

    def is_controlled(self) -> bool:
        return self.controlled

    def take_control(self) -> None:
        self.interrupt(True)
        actions.common.PlayerControl(self.owner).invoke()

    def interrupt(self, force: bool = False) -> None:
        self.ticket = None
        self.action = None
