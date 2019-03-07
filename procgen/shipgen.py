from __future__ import annotations

import sys

import itertools
import random
from typing import Any, Iterator, List, Optional, Tuple

import numpy as np  # type: ignore
import scipy.signal  # type: ignore
import tcod

from procgen.growingtree import AbstractGrowingTree
import engine.zone
import tiles
import obj.item


def np_sample(
    rng: random.Random, array: np.array, k: int,
) -> List[Tuple[Any, ...]]:
    if not np.any(array):
        return []
    return rng.sample(list(zip(*array.nonzero())), k)


class ProcGenException(Exception):
    pass


class NoRoom(ProcGenException):
    pass


class RoomType:
    priority: float = 0
    name: str = "<room>"
    floor: tiles.Tile = tiles.metal_floor
    wall: tiles.Tile = tiles.metal_wall
    min_size: Tuple[int, int] = (2, 2)
    max_size: Tuple[int, int] = (4, 4)

    def __lt__(self, other: RoomType) -> bool:
        return self.priority < other.priority

    def __str__(self) -> str:
        return self.name


class Corridor(RoomType):
    name = "Corridor"
    floor = tiles.metal_floor._replace(bg=(0x30, 0x30, 0x20))
    wall = tiles.metal_wall
    min_size = (1, 1)


class Space(RoomType):
    priority = 1
    name = "Space"
    floor = tiles.space
    wall = tiles.hull
    min_size = (1, 1)


class Hangar(RoomType):
    priority = 1
    name = "Hangar"
    floor = tiles.metal_floor._replace(bg=(0x00, 0x00, 0x20))
    wall = tiles.hull
    min_size = (8, 4)
    max_size = (8, 4)


class ShipRoomConntector(AbstractGrowingTree[Tuple[int, int, int]]):
    CARDINALS = ((-1, 0), (1, 0), (0, -1), (0, 1))

    def __init__(self, ship: Ship):
        self.ship = ship
        self.visited = ship.rooms == -1
        self.visited[self.ship.root_node] = True
        super().__init__()
        self.visit(self.ship.root_node, None)

    def grow(self) -> None:
        """Run a single step of the growing tree algorithm."""
        assert self.stem
        neighbors = list(self.get_all_neighbors())
        if not neighbors:
            self.stem = []
            return
        nodes, weights = zip(*neighbors)
        neighbor, stem = self.ship.rng.choices(list(nodes), weights)[0]
        self.visit(neighbor, stem)
        if not list(self.get_neighbors(stem)):
            self.stem.remove(stem)

    def get_all_neighbors(
        self,
    ) -> Iterator[Tuple[Tuple[Tuple[int, int, int],
                              Tuple[int, int, int]], int]]:
        for node in self.stem:
            for neighbor, weight in self.get_neighbors(node):
                yield (neighbor, node), weight

    def select_stem(self) -> int:
        return self.ship.rng.randint(0, len(self.stem) - 1)

    def select_neighbor(
        self, node: Tuple[int, int, int],
    ) -> Optional[Tuple[int, int, int]]:
        """Return an unvisited neighbor to `node` if one exists.

        This function should be overridden to set the behavior
        """
        neighbors = list(self.get_neighbors(node))
        if not neighbors:
            return None
        nodes, weights = zip(*self.get_neighbors(node))
        return self.ship.rng.choices(list(nodes), weights)[0]  # type: ignore

    def get_neighbors(
        self, node: Tuple[int, int, int],
    ) -> Iterator[Tuple[Tuple[int, int, int], int]]:
        """Generate an iterator of (neighbor, weight) tuples."""
        for x, y in self.CARDINALS:
            neighbor = node[0] + x, node[1] + y, node[2]
            if not(0 <= neighbor[0] < self.visited.shape[0]
                   and 0 <= neighbor[1] < self.visited.shape[1]):
                continue
            if self.visited[neighbor]:
                continue
            if self.ship.rooms[node] == self.ship.rooms[neighbor]:
                yield neighbor, 8
            yield neighbor, 1

    def get_room_type(self, node: Tuple[int, int, int]) -> RoomType:
        return self.ship.room_types[self.ship.rooms[node]]

    def visit(
        self,
        node: Tuple[int, int, int],
        prev: Optional[Tuple[int, int, int]],
    ) -> None:
        super().visit(node, prev)
        self.visited[node] = True
        if not list(self.get_neighbors(node)):
            self.stem.remove(node)
        if prev is None:
            return
        if prev[2] != node[2]:
            return
        if prev > node:  # Make sure prev is on the upper-left side of node.
            prev, node = node, prev

        if "--debug" in sys.argv:
            self.connect_rooms_debug(prev, node)
        else:
            self.connect_rooms(prev, node)

    def connect_rooms(
        self, room_a: Tuple[int, int, int], room_b: Tuple[int, int, int],
    ) -> None:
        door_x = room_b[0] * self.ship.room_width
        door_y = room_b[1] * self.ship.room_height
        if room_a[0] == room_b[0]:
            door_x += self.ship.rng.randint(1, self.ship.room_width - 1)
        else:
            assert room_a[1] == room_b[1]
            door_y += self.ship.rng.randint(1, self.ship.room_height - 1)
        door = door_x, door_y, room_b[2]
        self.ship.zone.data["tile"][door] = max(
            self.ship.room_types[self.ship.rooms[room_a]],
            self.ship.room_types[self.ship.rooms[room_b]],
        ).floor

    def connect_rooms_debug(
        self, room_a: Tuple[int, int, int], room_b: Tuple[int, int, int],
    ) -> None:
        line = tcod.line_where(
            room_a[0] * self.ship.room_width + 2,
            room_a[1] * self.ship.room_height + 2,
            room_b[0] * self.ship.room_width + 2,
            room_b[1] * self.ship.room_height + 2,
        )
        self.ship.zone.data["tile"][line] = \
            tiles.metal_floor._replace(bg=(0, 255, 0))


class Ship:
    start_position: Tuple[int, int, int]
    room_width = 4
    room_height = 4

    def __init__(self, seed: Optional[int] = None):
        if seed is None:
            seed = random.getrandbits(64)
        self.rng = random.Random(seed)
        self.generate()

    def generate(self) -> None:
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
            -1: Space(),
            0: RoomType(),
            1: Corridor(),
        }
        self.next_room_id = 2
        self.gen_form()
        self.gen_halls()
        # self.gen_rooms()
        self.add_new_room(Hangar(), 0)
        for size in range(5, 0, -1):
            try:
                while True:
                    self.add_new_room(RoomType())
            except NoRoom:
                pass
        self.rooms[self.rooms == 0] = 1

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
        self.root_node = start_x, self.half_width, 0
        self.start_position = (start_x * self.room_width + 1,
                               self.half_width * self.room_height + 1, 0)

    def new_room(self, room_type: Optional[RoomType] = None) -> int:
        if room_type is None:
            room_type = RoomType()
        self.room_types[self.next_room_id] = room_type
        self.next_room_id += 1
        return self.next_room_id - 1

    def add_room(
        self,
        room_id: int,
        size: Tuple[int, int],
        floor: int = 0,
    ) -> None:
        self.rooms[self.get_free_space(size, floor)] = room_id

    def add_new_room(self, room: RoomType, floor: int = 0) -> None:
        sizes = list(
            itertools.product(
                range(room.min_size[0], room.max_size[0] + 1),
                range(room.min_size[1], room.max_size[1] + 1),
            )
        )
        self.rng.shuffle(sizes)
        for size in sizes:
            try:
                self.rooms[self.get_free_space(size, 0)] = self.next_room_id
                break
            except NoRoom:
                pass
        else:
            raise NoRoom(f"Could not fit {room}.")
        self.room_types[self.next_room_id] = room
        self.next_room_id += 1

    def get_free_space(self, size: Tuple[int, int],
                       floor: int) -> Tuple[slice, slice]:
        """Return the slice indexes of a an unclaimed area."""
        width, height = size
        room_area = np.ones((width, height), dtype=bool)
        #  Convolve room_area into self.rooms, values of zero mean this room
        #  will fit.
        valid = scipy.signal.convolve(
            (self.rooms[..., floor] != 0).astype(int),
            room_area,
            "full",
        )[width-1:-width+1, height-1:-height+1]
        valid = np.transpose((valid == 0).nonzero())
        if not valid.size:
            raise NoRoom("No space left for room.")
        x, y = self.rng.choice(valid)
        assert (self.rooms[x:x+width, y:y+height, floor] == 0).all()
        return slice(x, x + width), slice(y, y + height)

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
                if rooms[0] is not room:
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

        self.zone.data["room_id"] = -1
        self.zone.data["room_id"][:-1, :-1, :] = np.kron(
            self.rooms, np.ones((self.room_width, self.room_height, 1))
        )
        self.zone.room_types = self.room_types

        ShipRoomConntector(self).generate()

        for room_id, room in self.room_types.items():
            if room_id == -1:
                continue
            area = self.zone.data["room_id"] == room_id
            area &= self.zone.data["tile"]["walkable"] != 0
            for xyz in np_sample(self.rng, area, 1):
                obj.item.Item(self.zone[xyz])  # type: ignore

    def show(self) -> str:
        def icon(x: int, y: int) -> str:
            if self.rooms[x, y] == -1:
                return " "
            else:
                return "%i" % (self.rooms[x, y, 0] % 10)

        return "\n".join("".join(icon(x, y) for x in range(self.length))
                         for y in range(self.width))
