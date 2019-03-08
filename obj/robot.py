from __future__ import annotations

import actions
import component.actor
import component.container
import component.graphic
import component.physicality
import component.verb
import obj.entity


class Robot(obj.entity.Entity):
    class Actor(component.actor.Actor):
        def act(self) -> actions.Action:
            return actions.Standby(self.owner)

    class Physicality(component.physicality.Physicality):
        name = "robot"

    class Container(component.container.Container):
        pass

    class Graphic(component.graphic.Graphic):
        CH = ord("R")

    class Interactable(component.verb.TakeControlInteractable):
        pass
