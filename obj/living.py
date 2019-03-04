
import actions
import component.actor
import obj.entity
import component.graphic


class Player(obj.entity.Entity):
    class Actor(component.actor.Player):
        pass

    class Graphic(component.graphic.Graphic):
        CH = ord("@")


class TestActor(obj.entity.Entity):
    class Actor(component.actor.Actor):
        def act(self) -> None:
            assert self.entity
            if not actions.Move(self.entity, (-1, 0, 0)).invoke():
                actions.Wait(self.entity).invoke()

    class Graphic(component.graphic.Graphic):
        CH = ord("T")
