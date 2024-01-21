from __future__ import annotations

import actions.base
import actions.combat
import actions.movement


class FightPlayer(actions.base.Action):
    def poll(self) -> actions.base.Action | None:
        action = actions.movement.Follow(self.entity, self.model.player).poll()
        if action:
            return action
        return actions.combat.Attack(self.entity, self.model.player).poll()
