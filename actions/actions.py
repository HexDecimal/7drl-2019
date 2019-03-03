from typing import Tuple

import engine.entity


class Action:
    def __init__(self, entity: engine.entity.Entity):
        self.entity = entity

    def invoke(self) -> bool:
        assert self.entity.actor
        # Ensure this actor was not already scheduled.
        assert self.entity.actor.ticket is None
        if not self.poll():
            return False
        interval = self.action()
        self.entity.actor.schedule(interval)
        return True

    def poll(self) -> bool:
        return True

    def action(self) -> int:
        raise NotImplementedError()


class Wait(Action):
    def action(self) -> int:
        return 100


class Move(Action):
    def __init__(
        self,
        entity: engine.entity.Entity,
        direction: Tuple[int, int, int],
    ):
        super().__init__(entity)
        self.direction = direction

    def poll(self) -> bool:
        new_loc = self.entity.location.get_relative(*self.direction)
        assert new_loc
        for obj in new_loc.contents:
            if obj.actor:
                return False
        return True

    def action(self) -> int:
        new_loc = self.entity.location.get_relative(*self.direction)
        self.entity.location = new_loc
        if self.direction[0] and self.direction[1]:
            return 150
        return 100


class Bump(Action):
    def __init__(
        self,
        entity: engine.entity.Entity,
        direction: Tuple[int, int, int],
    ) -> None:
        super().__init__(entity)
        self.direction = direction

    def poll(self) -> bool:
        return Move(self.entity, self.direction).poll()

    def action(self) -> int:
        return Move(self.entity, self.direction).action()
