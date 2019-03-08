from __future__ import annotations

from typing import Any, Tuple, Optional, TYPE_CHECKING

import g
import obj.entity
import component.graphic
if TYPE_CHECKING:
    import engine.zone


class Action:
    def __init__(self, entity: obj.entity.Entity):
        self.entity = entity

    def invoke(self) -> bool:
        """Attempt the action and return True if the action was performed."""
        assert self.entity.actor, "Action invoked on a non-actor entity."
        # Ensure this actor was not already scheduled.
        assert self.entity.actor.ticket is None, \
            "Actor is already waiting after an action."
        ready_action = self.poll()
        if ready_action is None:
            return False
        interval = ready_action.action()
        if interval is not None:
            self.entity.actor.schedule(interval)
        return True

    def poll(self) -> Optional[Action]:
        """Return an action which would be valid."""
        return self

    def action(self) -> Optional[int]:
        """Perform the action.

        This should never be called unless poll returns True.
        """
        raise NotImplementedError()

    def report(self, string: str, **format: Any) -> None:
        FORMAT = {
            "you": "you",
            "You": "You",
        }
        self.model.log.append(string.format(**FORMAT, **format))

    @property
    def zone(self) -> engine.zone.Zone:
        return self.entity.location.zone

    @property
    def model(self) -> engine.model.Model:
        return g.model


class LocationAction(Action):
    def __init__(
        self,
        entity: obj.entity.Entity,
        location: component.location.Location,
    ):
        super().__init__(entity)
        self.location = location


class EntityAction(Action):
    """Action with an entity target."""
    def __init__(
        self,
        entity: obj.entity.Entity,
        target: obj.entity.Entity,
    ):
        super().__init__(entity)
        self.target = target

    def poll(self) -> Optional[Action]:
        if self.target.is_alive():
            return self
        return None


class BumpAction(Action):
    """An action with a direction."""
    def __init__(
        self,
        entity: obj.entity.Entity,
        direction: Tuple[int, int, int],
    ):
        super().__init__(entity)
        self.direction = direction

    @property
    def destination(self) -> component.location.Location:
        """Return the location at the destination."""
        return self.entity.location.get_relative(*self.direction)
