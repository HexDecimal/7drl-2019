
import component.base


class Character(component.base.OwnedComponent):
    name = "character"
    attack_speed = 100
    move_speed = 100

    def __init__(self) -> None:
        self.hp = 100
