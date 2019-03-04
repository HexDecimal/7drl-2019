from typing import NamedTuple, Tuple

DTYPE = [
    ('ch', int),
    ('fg', '(3,)u1'),
    ('bg', '(3,)u1'),
    ("walkable", bool),
    ("transparent", bool),
]


class Tile(NamedTuple):
    ch: int = ord("?")
    fg: Tuple[int, int, int] = (255, 255, 255)
    bg: Tuple[int, int, int] = (0, 0, 0)
    walkable: bool = False
    transparent: bool = False


space = Tile(
    ch=ord(" "),
    bg=(0, 0, 0),
    walkable=True,
    transparent=True,
)

metal_floor = Tile(
    ch=ord("░"),
    fg=(0x28, 0x28, 0x30),
    bg=(0, 0, 0),
    walkable=True,
    transparent=True,
)
metal_wall = Tile(
    ch=ord(" "),
    bg=(0x70, 0x70, 0x80),
    walkable=False,
    transparent=False,
)
