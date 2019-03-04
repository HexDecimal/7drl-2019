from typing import Optional, TYPE_CHECKING

import component.base
if TYPE_CHECKING:
    import obj.entity


class Interactable(component.base.OwnedComponent):
    def interaction(self, entity: "obj.entity.Entity") -> Optional[int]:
        return 0


class TakeControlInteractable(Interactable):
    def interaction(self, entity: "obj.entity.Entity") -> Optional[int]:
        assert self.owner.actor
        assert entity.actor
        self.owner.actor.take_control()
        entity.actor.controlled = False
        return None
