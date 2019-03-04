from typing import TYPE_CHECKING

import component.base
if TYPE_CHECKING:
    import obj.entity


class Interactable(component.base.OwnedComponent):
    def interaction(self, entity: "obj.entity.Entity") -> None:
        pass


class TakeControlInteractable(Interactable):
    def interaction(self, entity: "obj.entity.Entity") -> None:
        assert self.owner.actor
        assert entity.actor
        self.owner.actor.controlled = True
        entity.actor.controlled = False
