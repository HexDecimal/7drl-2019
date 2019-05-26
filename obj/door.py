from __future__ import annotations

from typing import Optional

import actions.base
import component.graphic
import component.physicality
import component.verb
import obj.entity


class AutoDoor(obj.entity.Entity):
    class Physicality(component.physicality.Physicality):
        pass

    class Graphic(component.graphic.Graphic):
        CH = ord("+")

    class Interactable(component.verb.Interactable):
        class OpenDoor(actions.base.EntityAction):
            def poll(self) -> AutoDoor.Interactable.OpenDoor:
                return self

            def action(self) -> int:
                assert self.target.graphic
                assert self.target.physicality
                self.target.graphic = None
                self.target.physicality.blocking = False
                self.report("{You} open the door.")
                return 100

        def interaction(
            self, entity: obj.entity.Entity,
        ) -> Optional[actions.base.Action]:
            return self.OpenDoor(entity, self.owner)
