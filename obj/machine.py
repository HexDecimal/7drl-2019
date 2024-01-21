from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import component.container
import component.graphic
import component.physicality
import component.verb
import obj.entity

if TYPE_CHECKING:
    import actions.base


class Machine(obj.entity.Entity):
    class Physicality(component.physicality.Physicality):
        pass

    class Container(component.container.Container):
        pass

    class Graphic(component.graphic.Graphic):
        CH = ord("#")

    class Interactable(component.verb.Interaction):
        pass


class DriveCore(Machine):
    class Graphic(Machine.Graphic):
        CH = ord("╪")

    class Interactable(Machine.Interactable):
        class Action(Machine.Interactable.Action):
            def get_core(self) -> Optional[obj.entity.Entity]:
                assert self.entity.container
                for item in self.entity.container.contents:
                    if item.item and "drive core" in item.item.tags:
                        return item
                return None

            def poll(self) -> Optional[actions.base.Action]:
                assert self.entity.container
                if self.get_core():
                    return self
                return None

            def action(self) -> int:
                core = self.get_core()
                assert core
                assert self.target.container
                core.location = self.target.container.container
                self.report("{You} install the core.")
                return 100
