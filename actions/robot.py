from __future__ import annotations

from typing import Optional

import actions.base


class ReturnControlToPlayer(actions.base.Action):
    def poll(self) -> Optional[ReturnControlToPlayer]:
        if self.entity is self.model.player:
            return None
        return self

    def action(self) -> int:
        assert self.model.player.actor
        assert self.entity.actor
        self.entity.actor.controlled = False
        self.model.player.actor.take_control()
        self.report("{You} stop controlling the robot.")
        return 0


class RemoteControl(actions.base.EntityAction):
    def poll(self) -> Optional[actions.base.Action]:
        if self.target is self.model.player:
            return ReturnControlToPlayer(self.entity)
        return self

    def action(self) -> int:
        assert self.entity.actor
        assert self.target.actor
        self.entity.actor.controlled = False
        self.target.actor.take_control()
        self.report("{You} begin controlling the robot remotely.")
        return 0
