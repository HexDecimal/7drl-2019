import attrs


@attrs.define()
class Physicality:
    name: str = "character"
    attack_speed: int = 100
    move_speed: int = 100
    blocking: bool = True
    hp: int = 100
