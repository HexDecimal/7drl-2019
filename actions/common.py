from __future__ import annotations

from typing import Optional

import actions.base
import actions.combat
import actions.movement
import obj.entity
from component.verb import Interactable


class Wait(actions.base.Action):
    def action(self) -> int:
        return 100


class Interact(actions.base.EntityAction):
    def poll(self) -> Optional[actions.base.Action]:
        for interactable in self.target[Interactable]:
            return interactable.interaction(self.entity)
        return None


class BumpInteract(actions.base.BumpAction):
    def poll(self) -> Optional[actions.base.Action]:
        for target in self.destination.contents:
            for interactable in target[Interactable]:
                return Interact(self.entity, target).poll()
        return None


class Bump(actions.base.Action):
    def __init__(
        self,
        entity: obj.entity.Entity,
        direction: tuple[int, int, int],
    ) -> None:
        super().__init__(entity)
        self.direction = direction

    ACTIONS = (
        actions.movement.MoveBy,
        BumpInteract,
        actions.combat.BumpAttack,
    )

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


class Standby(actions.base.Action):
    def action(self) -> None:
        return None
