from typing import Tuple, Optional, TYPE_CHECKING

import obj.entity
import component.graphic
if TYPE_CHECKING:
    import component.location


class Action:
    def __init__(self, entity: obj.entity.Entity):
        self.entity = entity

    def invoke(self) -> bool:
        """Attempt the action and return True if the action was performed."""
        assert self.entity.actor, "Action invoked on a non-actor entity."
        # Ensure this actor was not already scheduled.
        assert self.entity.actor.ticket is None, \
            "Actor is already waiting after an action."
        if not self.poll():
            return False
        interval = self.action()
        self.entity.actor.schedule(interval)
        return True

    def poll(self) -> bool:
        """Return True if this action would be valid."""
        return True

    def action(self) -> int:
        """Perform the action.

        This should never be called unless poll returns True.
        """
        raise NotImplementedError()


class Wait(Action):
    def action(self) -> int:
        return 100


class BumpAction(Action):
    """An action with a direction."""
    def __init__(
        self,
        entity: obj.entity.Entity,
        direction: Tuple[int, int, int],
    ):
        super().__init__(entity)
        self.direction = direction

    def get_destination(self) -> "component.location.Location":
        """Return the location at the destination."""
        return self.entity.location.get_relative(*self.direction)


class Move(BumpAction):
    def poll(self) -> bool:
        dest = self.get_destination()
        if not dest.data["tile"]["walkable"]:
            return False
        for obj in dest.contents:
            if obj.actor:
                return False
        return True

    def action(self) -> int:
        self.entity.location = self.get_destination()
        if self.direction[0] and self.direction[1]:
            return 150
        return 100


class BumpAttack(BumpAction):
    def get_target(self) -> Optional[obj.entity.Entity]:
        for obj in self.get_destination().contents:
            if obj.actor:
                return obj
        return None

    def poll(self) -> bool:
        return bool(self.get_target())

    def action(self) -> int:
        target = self.get_target()
        assert target
        target.actor = None
        target.graphic = component.graphic.Graphic(ord('%'), (63, 63, 63))
        return 100


class Bump(Action):
    def __init__(
        self,
        entity: obj.entity.Entity,
        direction: Tuple[int, int, int],
    ) -> None:
        super().__init__(entity)
        self.direction = direction

    ACTIONS = (Move, BumpAttack)

    def poll(self) -> bool:
        for action_type in self.ACTIONS:
            if action_type(self.entity, self.direction).poll():
                return True
        return False

    def action(self) -> int:
        for action_type in self.ACTIONS:
            action = action_type(self.entity, self.direction)
            if action.poll():
                return action.action()
        assert False  # Will not be reached if poll returns True.
