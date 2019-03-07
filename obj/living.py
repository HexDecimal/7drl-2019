from __future__ import annotations

import component.actor
import component.character
import component.container
import component.graphic
import component.verb
import obj.entity


class Human(obj.entity.Entity):
    class Actor(component.actor.Actor):
        pass

    class Character(component.character.Character):
        name = "human"

    class Container(component.container.Container):
        pass

    class Graphic(component.graphic.Graphic):
        CH = ord("U")


class Player(Human):
    class Actor(Human.Actor):
        controlled = True

    class Character(Human.Character):
        name = "you"

    class Graphic(Human.Graphic):
        CH = ord("@")

    class Interactable(component.verb.TakeControlInteractable):
        pass
