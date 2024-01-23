from __future__ import annotations

import tcod.ecs

import component.actor
import component.graphic
import component.location
import g
from actions import ActionLike
from component.location import Location
from component.physicality import Physicality


class Action(ActionLike):
    def __init__(self, entity: tcod.ecs.Entity) -> None:
        self.entity = entity

    def invoke(self) -> bool:
        """Attempt the action and return True if the action was performed."""
        # Ensure this actor was not already scheduled.
        assert self.entity.components[component.actor.Actor].ticket is None, "Actor is already waiting after an action."
        ready_action = self.poll()
        if ready_action is None:
            return False
        interval = ready_action.action()
        if interval is not None:
            self.entity.components[component.actor.Actor].schedule(self.entity, interval)
        return True

    def poll(self) -> Action | None:
        """Return an action which would be valid."""
        return self

    def action(self) -> int | None:
        """Perform the action.

        This should never be called unless poll returns True.
        """
        raise NotImplementedError()

    def report(self, string: str, **format: object) -> None:
        FORMAT = {
            "you": "you",
            "You": "You",
        }
        g.world[None].components[("log", list[str])].append(string.format(**FORMAT, **format))


class LocationAction(Action):
    def __init__(
        self,
        entity: tcod.ecs.Entity,
        location: Location,
    ) -> None:
        super().__init__(entity)
        self.location = location


class EntityAction(Action):
    """Action with an entity target."""

    def __init__(
        self,
        entity: tcod.ecs.Entity,
        target: tcod.ecs.Entity,
    ) -> None:
        super().__init__(entity)
        self.target = target

    def poll(self) -> Action | None:
        if Physicality in self.target.components:
            return self
        return None


class BumpAction(Action):
    """An action with a direction."""

    def __init__(
        self,
        entity: tcod.ecs.Entity,
        direction: tuple[int, int, int],
    ) -> None:
        super().__init__(entity)
        self.direction = direction

    @property
    def destination(self) -> Location:
        """Return the location at the destination."""
        return self.entity.components[Location].get_relative(*self.direction)
