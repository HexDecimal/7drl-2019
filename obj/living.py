from __future__ import annotations

import actions
import component.actor
import component.container
import component.graphic
import component.verb
import g
import obj.entity


class Player(obj.entity.Entity):
    class Actor(component.actor.Actor):
        controlled = True

    class Container(component.container.Container):
        pass

    class Graphic(component.graphic.Graphic):
        CH = ord("@")

    class Interactable(component.verb.TakeControlInteractable):
        pass


class TestActor(obj.entity.Entity):
    class Actor(component.actor.Actor):
        def act(self) -> actions.Action:
            if g.model.player:
                return actions.Follow(self.owner, g.model.player)
            return actions.Wait(self.owner)

    class Graphic(component.graphic.Graphic):
        CH = ord("T")


class TestRobot(obj.entity.Entity):
    class Actor(component.actor.Actor):
        def act(self) -> actions.Action:
            return actions.Standby(self.owner)

    class Container(component.container.Container):
        pass

    class Graphic(component.graphic.Graphic):
        CH = ord("R")

    class Interactable(component.verb.TakeControlInteractable):
        pass
