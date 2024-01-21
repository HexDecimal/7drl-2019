from __future__ import annotations

from typing import TYPE_CHECKING

import actions.base
import actions.robot
import component.base

if TYPE_CHECKING:
    import obj.entity


class Interactable(component.base.OwnedComponent):
    def interaction(
        self,
        entity: obj.entity.Entity,
    ) -> actions.base.Action | None:
        return None


class TakeControlInteractable(Interactable):
    def interaction(
        self,
        entity: obj.entity.Entity,
    ) -> actions.base.Action | None:
        return actions.robot.RemoteControl(entity, self.owner).poll()


class Interaction(Interactable):
    class Action(actions.base.EntityAction):
        pass

    def interaction(
        self,
        entity: obj.entity.Entity,
    ) -> actions.base.Action | None:
        return self.Action(entity, self.owner).poll()
