from __future__ import annotations

import random
from typing import Iterator, NamedTuple, Optional, Tuple

import numpy as np  # type: ignore
import scipy.signal  # type: ignore

import engine.zone
import tiles


class RoomType(NamedTuple):
    priority: float = 0
    floor: tiles.Tile = tiles.metal_floor
    wall: tiles.Tile = tiles.metal_wall


class Ship:
    start_position: Tuple[int, int, int]
    room_width = 4
    room_height = 4

    def __init__(self, seed: Optional[int] = None):
        if seed is None:
            seed = random.getrandbits(64)
        self.rng = random.Random(seed)
        self.length = 64
        self.half_width = 8
        self.depth = 1
        self.width = self.half_width * 2 + self.rng.randint(0, 1)
        self.zone = engine.zone.Zone((self.length * self.room_width + 1,
                                      self.width * self.room_height + 1,
                                      self.depth))

        self.form = np.zeros((self.depth, self.length), dtype=int)
        self.rooms = np.zeros((self.length, self.width, self.depth),
                              dtype=int, order="F")
        self.room_types = {
            -1: RoomType(1, tiles.space, tiles.metal_wall),
            0: RoomType(0, tiles.metal_floor, tiles.metal_wall),
            1: RoomType(0, tiles.metal_floor._replace(bg=(0x30, 0x30, 0x20)),
                        tiles.metal_wall),
        }
        self.gen_form()
        self.gen_halls()
        # self.gen_rooms()
        self.finalize()

    def gen_form(self) -> None:
        x = 0
        while x < self.length:
            xx = x + self.rng.randint(1, self.width)
            self.form[:, x:xx] = \
                self.rng.randint(0, int(self.half_width // 1.5))
            x = xx

        for x in range(self.length):
            if self.form[0, x] == 0:
                continue
            self.rooms[x, :self.form[0, x], 0] = -1
            self.rooms[x, -self.form[0, x]:, 0] = -1

    def gen_halls(self) -> None:
        start_x = self.rng.randint(0, self.length // 4)
        end_x = self.rooms.shape[0] - self.rng.randint(0, self.length // 4)
        self.rooms[start_x:end_x, self.half_width, 0] = 1
        self.start_position = (start_x * self.room_width + 1,
                               self.half_width * self.room_height + 1, 0)

    def gen_rooms(self) -> None:
        i = 2
        sizes = [(3, 3), (2, 3), (3, 2), (2, 2,), (1, 2), (2, 1), (1, 1)]
        for y in range(self.rooms.shape[1]):
            for x in range(self.rooms.shape[0]):
                if self.rooms[x, y, 0] != 0:
                    continue
                self.rng.shuffle(sizes)
                for width, height in sizes:
                    area = self.rooms[x:x+width, y:y+height, 0]
                    if (area != 0).any():
                        continue
                    area[...] = i
                i += 1

    def get_unclaimed_cell(self) -> Tuple[int, int]:
        nz = self.get_unclaimed_cells().nonzero()
        i = self.rng.randint(0, len(nz[0]) - 1)
        return nz[0][i], nz[1][i]

    def get_unclaimed_cells(self) -> np.array:
        claimed = self.rooms > 0
        free = self.rooms == 0
        neigbors = scipy.signal.convolve(
            in1=claimed,
            in2=[
                [0, 1, 0],
                [1, 0, 1],
                [0, 1, 0],
            ],
            mode="same",
        )
        return (neigbors != 0) & free

    def finalize(self) -> None:
        def get_room_type(cx: int, cy: int, cz: int) -> RoomType:
            if 0 <= cx < self.rooms.shape[0] and 0 <= cy < self.rooms.shape[1]:
                return self.room_types[self.rooms[cx, cy, cz]]
            return self.room_types[-1]

        def iter_cells() -> Iterator[Tuple[int, int, int]]:
            for z in range(self.rooms.shape[2]):
                for y in range(self.rooms.shape[1] + 1):
                    for x in range(self.rooms.shape[0] + 1):
                        yield x, y, z

        def get_merge_tile(*rooms: RoomType) -> tiles.Tile:
            for room in rooms[1:]:
                if rooms[0] != room:
                    break
            else:
                return rooms[0].floor
            return max(rooms).wall

        for cx, cy, cz in iter_cells():
            room_type = get_room_type(cx, cy, cz)
            left_type = get_room_type(cx - 1, cy, cz)
            top_type = get_room_type(cx, cy - 1, cz)
            topleft_type = get_room_type(cx - 1, cy - 1, cz)

            left = cx * self.room_width
            top = cy * self.room_height
            right = left + self.room_width
            bottom = top + self.room_height

            left_tile = get_merge_tile(room_type, left_type)
            top_tile = get_merge_tile(room_type, top_type)
            topleft_tile = get_merge_tile(room_type, left_type,
                                          top_type, topleft_type)

            self.zone.data["tile"][left, top, cz] = topleft_tile
            self.zone.data["tile"][left+1:right, top, cz] = top_tile
            self.zone.data["tile"][left, top+1:bottom, cz] = left_tile
            self.zone.data["tile"][left+1:right, top+1:bottom, cz] = \
                room_type.floor

    def show(self) -> str:
        def icon(x: int, y: int) -> str:
            if self.rooms[x, y] == -1:
                return " "
            else:
                return "%i" % (self.rooms[x, y, 0] % 10)

        return "\n".join("".join(icon(x, y) for x in range(self.length))
                         for y in range(self.width))
