from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import actions.robot
import component.base
if TYPE_CHECKING:
    import actions.base
    import obj.entity


class Interactable(component.base.OwnedComponent):
    def interaction(
        self, entity: obj.entity.Entity,
    ) -> Optional[actions.base.Action]:
        return None


class TakeControlInteractable(Interactable):
    def interaction(
        self, entity: obj.entity.Entity,
    ) -> Optional[actions.base.Action]:
        return actions.robot.RemoteControl(entity, self.owner).poll()
