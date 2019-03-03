
import engine.actor
import engine.entity
import engine.graphic


class Player(engine.entity.Entity):
    class Actor(engine.actor.Player):
        pass

    class Graphic(engine.graphic.Graphic):
        CH = ord("@")
