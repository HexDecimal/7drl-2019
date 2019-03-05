from __future__ import annotations

from typing import Tuple, Optional, TYPE_CHECKING

import actions.base
import actions.movement
import g
import obj.entity
import component.graphic
if TYPE_CHECKING:
    import component.location


class Wait(actions.base.Action):
    def action(self) -> int:
        return 100


class Attack(actions.base.EntityAction):
    def action(self) -> int:
        self.target.actor = None
        self.target.graphic = component.graphic.Graphic(ord('%'), (63, 63, 63))
        return 100


class BumpAttack(actions.base.BumpAction):
    def poll(self) -> Optional[actions.base.Action]:
        for target in self.destination.contents:
            if target.actor:
                return Attack(self.entity, target).poll()
        return None


class Interact(actions.base.EntityAction):
    def action(self) -> int:
        assert self.target.interactable
        self.target.interactable.interaction(self.entity)
        return 0


class BumpInteract(actions.base.BumpAction):
    def poll(self) -> Optional[actions.base.Action]:
        for target in self.destination.contents:
            if target.interactable:
                return Interact(self.entity, target).poll()
        return None


class Bump(actions.base.Action):
    def __init__(
        self,
        entity: obj.entity.Entity,
        direction: Tuple[int, int, int],
    ) -> None:
        super().__init__(entity)
        self.direction = direction

    ACTIONS = (actions.movement.MoveBy, BumpInteract, BumpAttack)

    def poll(self) -> Optional[actions.base.Action]:
        for action_type in self.ACTIONS:
            action = action_type(self.entity, self.direction).poll()
            if action is not None:
                return action
        return None


class PlayerControl(actions.base.Action):
    """Give immediate user control to this entity."""
    def action(self) -> Optional[int]:
        assert self.entity
        assert self.entity.actor
        self.entity.actor.controlled = True
        self.entity.location.zone.camera = self.entity.location.xyz
        self.entity.location.zone.player = self.entity
        return None  # Further actions will be pending.


class ReturnControlToPlayer(actions.base.Action):
    def action(self) -> int:
        assert g.model.player.actor
        assert self.entity.actor
        self.entity.actor.controlled = False
        g.model.player.actor.take_control()
        return 0


class Standby(actions.base.Action):
    def action(self) -> None:
        return None
