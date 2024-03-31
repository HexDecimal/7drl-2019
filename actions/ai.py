from __future__ import annotations

import attrs
import tcod.ecs

import actions.base
import actions.combat
import actions.movement
from actions import ActionResult
from engine.helpers import active_player


@attrs.define()
class FightPlayer:
    def perform(self, entity: tcod.ecs.Entity) -> ActionResult:
        action = actions.movement.Follow(active_player()).perform(entity)
        if action:
            return action
        return actions.combat.Attack(active_player()).perform(entity)
