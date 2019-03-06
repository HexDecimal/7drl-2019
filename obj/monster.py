from __future__ import annotations

import actions.ai
import component.actor
import component.character
import component.container
import component.graphic
import component.verb
import obj.entity


class Monster(obj.entity.Entity):
    class Actor(component.actor.Actor):
        def act(self) -> actions.Action:
            return actions.ai.FightPlayer(self.owner)

    class Character(component.character.Character):
        name = "alien"

    class Container(component.container.Container):
        pass

    class Graphic(component.graphic.Graphic):
        CH = ord("a")
