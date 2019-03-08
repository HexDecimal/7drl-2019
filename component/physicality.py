
import component.base


class Physicality(component.base.OwnedComponent):
    name = "character"
    attack_speed = 100
    move_speed = 100
    blocking = True

    def __init__(self) -> None:
        self.hp = 100
