
import actions
import engine.actor
import engine.entity
import engine.graphic


class Player(engine.entity.Entity):
    class Actor(engine.actor.Player):
        pass

    class Graphic(engine.graphic.Graphic):
        CH = ord("@")


class TestActor(engine.entity.Entity):
    class Actor(engine.actor.Actor):
        def act(self) -> None:
            assert self.entity
            if not actions.Move(self.entity, (-1, 0, 0)).invoke():
                actions.Wait(self.entity).invoke()

    class Graphic(engine.graphic.Graphic):
        CH = ord("T")
