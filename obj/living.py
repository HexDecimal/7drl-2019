
import actions
import component.actor
import component.graphic
import component.verb
import obj.entity


class Player(obj.entity.Entity):
    class Actor(component.actor.Player):
        pass

    class Graphic(component.graphic.Graphic):
        CH = ord("@")

    Interactable = component.verb.TakeControlInteractable


class TestActor(obj.entity.Entity):
    class Actor(component.actor.Actor):
        def act(self) -> None:
            if not actions.Move(self.owner, (-1, 0, 0)).invoke():
                actions.Wait(self.owner).invoke()

    class Graphic(component.graphic.Graphic):
        CH = ord("T")


class TestRobot(obj.entity.Entity):
    class Actor(component.actor.Robot):
        pass

    class Graphic(component.graphic.Graphic):
        CH = ord("R")

    Interactable = component.verb.TakeControlInteractable
