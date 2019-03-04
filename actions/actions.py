from typing import Tuple, Optional, TYPE_CHECKING

import tcod.path

import g
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
        assert self.entity.actor.action is None, \
            "Actor already has an action."
        assert self.entity.actor.ticket is None, \
            "Actor is already waiting after an action."
        ready_action = self.poll()
        if ready_action is None:
            return False
        self.entity.actor.action = self
        interval = ready_action.action()
        if interval is not None:
            self.entity.actor.schedule(interval)
        return True

    def poll(self) -> Optional["Action"]:
        """Return an action which would be valid."""
        return self

    def action(self) -> Optional[int]:
        """Perform the action.

        This should never be called unless poll returns True.
        """
        raise NotImplementedError()


class Wait(Action):
    def action(self) -> int:
        return 100


class TargetAction(Action):
    """Action with an entity target."""
    def __init__(
        self,
        entity: obj.entity.Entity,
        target: obj.entity.Entity,
    ):
        super().__init__(entity)
        self.target = target

    def poll(self) -> Optional["Action"]:
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

    def get_destination(self) -> "component.location.Location":
        """Return the location at the destination."""
        return self.entity.location.get_relative(*self.direction)


class Move(BumpAction):
    def poll(self) -> Optional["Action"]:
        dest = self.get_destination()
        if not dest.data["tile"]["walkable"]:
            return None
        for entity in dest.contents:
            if entity.actor:
                return None
        return self

    def action(self) -> int:
        self.entity.location = self.get_destination()
        if self.direction[0] and self.direction[1]:
            return 150
        return 100


class BumpAttack(BumpAction):
    def get_target(self) -> Optional[obj.entity.Entity]:
        for entity in self.get_destination().contents:
            if entity.actor:
                return entity
        return None

    def poll(self) -> Optional["Action"]:
        if self.get_target():
            return self
        return None

    def action(self) -> int:
        target = self.get_target()
        assert target
        target.actor = None
        target.graphic = component.graphic.Graphic(ord('%'), (63, 63, 63))
        return 100


class BumpInteract(BumpAction):
    def get_target(self) -> Optional[obj.entity.Entity]:
        for entity in self.get_destination().contents:
            if entity.interactable:
                return entity
        return None

    def poll(self) -> Optional["Action"]:
        if self.get_target():
            return self
        return None

    def action(self) -> int:
        target = self.get_target()
        assert target and target.interactable
        target.interactable.interaction(self.entity)
        return 0


class Bump(Action):
    def __init__(
        self,
        entity: obj.entity.Entity,
        direction: Tuple[int, int, int],
    ) -> None:
        super().__init__(entity)
        self.direction = direction

    ACTIONS = (Move, BumpInteract, BumpAttack)

    def poll(self) -> Optional[Action]:
        for action_type in self.ACTIONS:
            action = action_type(self.entity, self.direction).poll()
            if action is not None:
                return action
        return None


class PlayerControl(Action):
    """Give immediate user control to this entity."""
    def action(self) -> Optional[int]:
        assert self.entity
        assert self.entity.actor
        self.entity.actor.controlled = True
        self.entity.location.zone.camera = self.entity.location.xyz
        self.entity.location.zone.player = self.entity
        return None  # Further actions will be pending.


class ReturnControlToPlayer(Action):
    def action(self) -> int:
        assert g.player.actor
        assert self.entity.actor
        self.entity.actor.controlled = False
        g.player.actor.take_control()
        return 0


class Standby(Action):
    def action(self) -> None:
        return None


class Follow(TargetAction):
    def __init__(
        self,
        entity: obj.entity.Entity,
        target: obj.entity.Entity,
    ):
        super().__init__(entity, target)
        z = entity.location.xyz[2]
        self.pathfinder = tcod.path.AStar(
            entity.location.zone.data["tile"]["walkable"][:, :, z],
        )

    def poll(self) -> Optional[Action]:
        my_coord = self.entity.location.xyz[:2]
        target_coord = self.target.location.xyz[:2]
        path = self.pathfinder.get_path(*my_coord, *target_coord)
        if len(path) >= 2:
            return Move(
                self.entity,
                (path[0][0] - my_coord[0], path[0][1] - my_coord[1],  0),
            ).poll()
        else:
            return Wait(self.entity).poll()
