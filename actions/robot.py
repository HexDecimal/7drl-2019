from __future__ import annotations

import actions.base
import component.actor
from engine.helpers import active_player


class ReturnControlToPlayer(actions.base.Action):
    def poll(self) -> ReturnControlToPlayer | None:
        if self.entity is active_player():
            return None
        return self

    def action(self) -> int:
        player = active_player()
        self.entity.components[component.actor.Actor].controlled = False
        component.actor.Actor.take_control(player)
        self.report("{You} stop controlling the robot.")
        return 0


class RemoteControl(actions.base.EntityAction):
    def poll(self) -> actions.base.Action | None:
        if self.target is active_player():
            return ReturnControlToPlayer(self.entity)
        return self

    def action(self) -> int:
        self.entity.components[component.actor.Actor].controlled = False
        component.actor.Actor.take_control(self.target)
        self.report("{You} begin controlling the robot remotely.")
        return 0
