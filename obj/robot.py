from __future__ import annotations

import actions
import component.actor
import component.character
import component.container
import component.graphic
import component.verb
import obj.entity


class Robot(obj.entity.Entity):
    class Actor(component.actor.Actor):
        def act(self) -> actions.Action:
            return actions.Standby(self.owner)

    class Character(component.character.Character):
        name = "robot"

    class Container(component.container.Container):
        pass

    class Graphic(component.graphic.Graphic):
        CH = ord("R")

    class Interactable(component.verb.TakeControlInteractable):
        pass
