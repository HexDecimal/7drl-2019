from __future__ import annotations

import actions.ai
import actions.base
import component.actor
import component.container
import component.graphic
import component.physicality
import component.verb
import obj.entity


class Monster(obj.entity.Entity):
    class Actor(component.actor.Actor):
        def act(self) -> actions.base.Action:
            return actions.ai.FightPlayer(self.owner)

    class Physicality(component.physicality.Physicality):
        name = "alien"

    class Container(component.container.Container):
        pass

    class Graphic(component.graphic.Graphic):
        CH = ord("a")
