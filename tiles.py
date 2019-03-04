from __future__ import annotations

from typing import NamedTuple, Tuple

DTYPE = [
    ('ch', int),
    ('fg', '(3,)u1'),
    ('bg', '(3,)u1'),
    ("walkable", int),
    ("transparent", bool),
]


class Tile(NamedTuple):
    ch: int = ord("?")
    fg: Tuple[int, int, int] = (255, 255, 255)
    bg: Tuple[int, int, int] = (0, 0, 0)
    walkable: int = 0
    transparent: bool = False


space = Tile(
    ch=ord(" "),
    bg=(0, 0, 0),
    walkable=1,
    transparent=True,
)

metal_floor = Tile(
    ch=ord("░"),
    fg=(0x28, 0x28, 0x30),
    bg=(0, 0, 0),
    walkable=1,
    transparent=True,
)
metal_wall = Tile(
    ch=ord(" "),
    bg=(0x70, 0x70, 0x80),
    walkable=0,
    transparent=False,
)
