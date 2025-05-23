from __future__ import annotations

import itertools
import random
import sys
from collections.abc import Iterator
from typing import Any

import numpy as np
import scipy.signal  # type: ignore[import-untyped]
import tcod.ecs
import tcod.libtcodpy
from numpy.typing import NDArray

import engine.zone
import g
import obj.door
import obj.item
import obj.living
import obj.machine
import obj.robot
import tiles
from procgen.growing_tree import AbstractGrowingTree


class ProcGenError(Exception):
    pass


class NoRoomError(ProcGenError):
    pass


class RoomType:
    priority: float = 0
    name: str = "<room>"
    floor: tiles.Tile = tiles.metal_floor
    wall: tiles.Tile = tiles.metal_wall
    min_size: tuple[int, int] = (2, 2)
    max_size: tuple[int, int] = (4, 4)

    def __lt__(self, other: RoomType) -> bool:
        return self.priority < other.priority

    def __str__(self) -> str:
        return self.name

    def get_area(self, room_id: int, ship: Ship) -> NDArray[np.bool_]:
        area: NDArray[np.bool_] = ship.zone.data["room_id"] == room_id
        area &= ship.zone.data["tile"]["walkable"] != 0
        return area

    def finalize(self, room_id: int, ship: Ship) -> None:
        for xyz in ship.np_sample(self.get_area(room_id, ship), 1):
            obj.item.new_item(g.world, ship.zone[xyz])


class Corridor(RoomType):
    priority = -1
    name = "Corridor"
    floor = tiles.metal_floor._replace(bg=(0x30, 0x30, 0x20))
    wall = tiles.metal_wall
    min_size = (1, 1)


class Space(RoomType):
    priority = 100
    name = "Space"
    floor = tiles.space
    wall = tiles.hull
    min_size = (1, 1)

    def finalize(self, room_id: int, ship: Ship) -> None:
        pass


class Hangar(RoomType):
    priority = 1
    name = "Hangar"
    floor = tiles.metal_floor._replace(bg=(0x00, 0x00, 0x20))
    wall = tiles.reinforced_wall
    min_size = (8, 4)
    max_size = (8, 4)

    def finalize(self, room_id: int, ship: Ship) -> None:
        pos1, pos2 = ship.np_sample(self.get_area(room_id, ship), 2)
        ship.player = obj.living.new_player(g.world, ship.zone[pos1])
        obj.robot.new_robot(g.world, ship.zone[pos2])


class BasePowerRoom(RoomType):
    floor = RoomType.floor._replace(bg=(0x30, 0x30, 0x00))
    min_size = (2, 2)
    max_size = (3, 3)


class DriveCore(BasePowerRoom):
    priority = 1
    name = "Drive Core"
    wall = tiles.reinforced_wall
    min_size = (3, 3)
    max_size = (4, 4)

    def finalize(self, room_id: int, ship: Ship) -> None:
        pos1, pos2 = ship.np_sample(self.get_area(room_id, ship), 2)
        obj.machine.new_drive_core(g.world, ship.zone[pos1])
        obj.item.new_spare_core(g.world, ship.zone[pos2])


class Solars(BasePowerRoom):
    name = "Solars"


class Nuclear(BasePowerRoom):
    priority = 1
    name = "Nuclear"
    wall = tiles.reinforced_wall


class Bridge(RoomType):
    name = "Bridge"
    floor = RoomType.floor._replace(bg=(0x30, 0x30, 0x30))
    min_size = (2, 2)
    max_size = (4, 4)


class ShipRoomConnector(AbstractGrowingTree[tuple[int, int, int]]):
    CARDINALS = ((-1, 0), (1, 0), (0, -1), (0, 1))

    def __init__(self, ship: Ship) -> None:
        self.ship = ship
        self.visited = ship.rooms == -1
        self.visited[self.ship.root_node] = True
        super().__init__()
        # Connected rooms: Tuple[axis, index, room_id1, room_id2]
        self.connected: set[tuple[int, int, int, int]] = set()
        self.visit(self.ship.root_node, None)

    def grow(self) -> None:
        """Run a single step of the growing tree algorithm."""
        assert self.stem
        neighbors = list(self.get_all_neighbors())
        if not neighbors:
            self.stem = []
            return
        nodes, weights = zip(*neighbors, strict=True)
        neighbor, stem = self.ship.rng.choices(list(nodes), weights)[0]
        self.visit(neighbor, stem)
        if not list(self.get_neighbors(stem)):
            self.stem.remove(stem)

    def get_all_neighbors(
        self,
    ) -> Iterator[tuple[tuple[tuple[int, int, int], tuple[int, int, int]], int]]:
        for node in self.stem:
            for neighbor, weight in self.get_neighbors(node):
                yield (neighbor, node), weight

    def select_stem(self) -> int:
        return self.ship.rng.randint(0, len(self.stem) - 1)

    def select_neighbor(
        self,
        node: tuple[int, int, int],
    ) -> tuple[int, int, int] | None:
        """Return an unvisited neighbor to `node` if one exists.

        This function should be overridden to set the behavior
        """
        neighbors = list(self.get_neighbors(node))
        if not neighbors:
            return None
        nodes, weights = zip(*self.get_neighbors(node), strict=True)
        return self.ship.rng.choices(list(nodes), weights)[0]  # type: ignore[no-any-return]

    def get_connection(
        self,
        node1: tuple[int, int, int],
        node2: tuple[int, int, int],
    ) -> tuple[int, int, int, int]:
        """Returns Tuple[axis, index, room_id1, room_id2]."""
        node1, node2 = sorted((node1, node2))
        assert node1[2] == node2[2]
        if node1[1] == node2[1]:
            assert node1[0] != node2[0]
            axis = 0
        else:
            assert node1[0] == node2[0]
            assert node1[1] != node2[1]
            axis = 1
        return (axis, node1[axis], self.ship.rooms[node1], self.ship.rooms[node2])

    def get_neighbors(
        self,
        node: tuple[int, int, int],
    ) -> Iterator[tuple[tuple[int, int, int], int]]:
        """Generate an iterator of (neighbor, weight) tuples."""
        for x, y in self.CARDINALS:
            neighbor = node[0] + x, node[1] + y, node[2]
            if not (0 <= neighbor[0] < self.visited.shape[0] and 0 <= neighbor[1] < self.visited.shape[1]):
                continue
            if self.visited[neighbor]:
                continue
            if self.ship.rooms[node] == self.ship.rooms[neighbor]:
                yield neighbor, 500
            yield neighbor, 1

    def get_room_type(self, node: tuple[int, int, int]) -> RoomType:
        return self.ship.room_types[self.ship.rooms[node]]

    def visit(
        self,
        node: tuple[int, int, int],
        prev: tuple[int, int, int] | None,
    ) -> None:
        super().visit(node, prev)
        self.visited[node] = True
        if not list(self.get_neighbors(node)):
            self.stem.remove(node)
        if prev is None:
            return
        if prev[2] != node[2]:
            return
        # Make sure prev is on the upper-left side of node.
        prev, node = sorted((prev, node))

        connection = self.get_connection(prev, node)
        # assert connection not in self.connected
        self.connected.add(connection)

        if "--debug" in sys.argv:
            self.connect_rooms_debug(prev, node)
        else:
            self.connect_rooms(prev, node)

    def connect_rooms(
        self,
        room_a: tuple[int, int, int],
        room_b: tuple[int, int, int],
    ) -> None:
        door_x = room_b[0] * self.ship.room_width
        door_y = room_b[1] * self.ship.room_height
        if room_a[0] == room_b[0]:
            door_x += self.ship.rng.randint(1, self.ship.room_width - 1)
        else:
            assert room_a[1] == room_b[1]
            door_y += self.ship.rng.randint(1, self.ship.room_height - 1)
        door = door_x, door_y, room_b[2]
        if self.ship.zone.data["tile"]["walkable"][door]:
            return
        self.ship.zone.data["tile"][door] = max(
            self.ship.room_types[self.ship.rooms[room_a]],
            self.ship.room_types[self.ship.rooms[room_b]],
        ).floor
        obj.door.new_auto_door(g.world, self.ship.zone[door])

    def connect_rooms_debug(
        self,
        room_a: tuple[int, int, int],
        room_b: tuple[int, int, int],
    ) -> None:
        line = tcod.libtcodpy.line_where(
            room_a[0] * self.ship.room_width + 2,
            room_a[1] * self.ship.room_height + 2,
            room_b[0] * self.ship.room_width + 2,
            room_b[1] * self.ship.room_height + 2,
        )
        self.ship.zone.data["tile"][line] = tiles.metal_floor._replace(bg=(0, 255, 0))


class Ship:
    start_position: tuple[int, int, int]
    player: tcod.ecs.Entity
    room_width = 4
    room_height = 4

    def __init__(self, seed: int | None = None) -> None:
        if seed is None:
            seed = random.getrandbits(64)
        self.rng = random.Random(seed)
        self.generate()

    def np_sample(self, array: NDArray[Any], k: int) -> list[tuple[Any, ...]]:
        if not np.any(array):
            return []
        return self.rng.sample(list(zip(*array.nonzero(), strict=False)), k)

    def generate(self) -> None:
        self.length = 64
        self.half_width = 8
        self.depth = 1
        self.width = self.half_width * 2 + self.rng.randint(0, 1)
        self.zone = engine.zone.Zone((self.length * self.room_width + 1, self.width * self.room_height + 1, self.depth))
        g.world[None].components[engine.zone.Zone] = self.zone

        self.form = np.zeros((self.depth, self.length), dtype=int)
        self.rooms = np.zeros((self.length, self.width, self.depth), dtype=int, order="F")
        self.room_types = {
            -1: Space(),
            0: RoomType(),
            1: Corridor(),
        }
        self.next_room_id = 2
        self.gen_form()
        self.gen_halls()
        vital_rooms = [
            Hangar,
            DriveCore,
            Solars,
            Nuclear,
            Bridge,
        ]
        for room_cls in vital_rooms:
            self.add_new_room(room_cls(), 0)
        try:
            while True:
                self.add_new_room(RoomType())
        except NoRoomError:
            pass
        self.rooms[self.rooms == 0] = 1

        self.finalize()

    def gen_form(self) -> None:
        x = 0
        while x < self.length:
            xx = x + self.rng.randint(1, self.width)
            self.form[:, x:xx] = self.rng.randint(0, int(self.half_width // 1.5))
            x = xx

        for x in range(self.length):
            if self.form[0, x] == 0:
                continue
            self.rooms[x, : self.form[0, x], 0] = -1
            self.rooms[x, -self.form[0, x] :, 0] = -1

    def gen_halls(self) -> None:
        start_x = self.rng.randint(0, self.length // 4)
        end_x = self.rooms.shape[0] - self.rng.randint(0, self.length // 4)
        self.rooms[start_x:end_x, self.half_width, 0] = 1
        self.root_node = start_x, self.half_width, 0
        self.start_position = (start_x * self.room_width + 1, self.half_width * self.room_height + 1, 0)

    def add_new_room(self, room: RoomType, floor: int = 0) -> None:  # noqa: ARG002
        sizes = list(
            itertools.product(
                range(room.min_size[0], room.max_size[0] + 1),
                range(room.min_size[1], room.max_size[1] + 1),
            ),
        )
        self.rng.shuffle(sizes)
        for size in sizes:
            try:
                self.rooms[self.get_free_space(size, 0)] = self.next_room_id
                break
            except NoRoomError:
                pass
        else:
            msg = f"Could not fit {room}."
            raise NoRoomError(msg)
        self.room_types[self.next_room_id] = room
        self.next_room_id += 1

    def get_free_space(self, size: tuple[int, int], floor: int) -> tuple[slice, slice]:
        """Return the slice indexes of a an unclaimed area."""
        width, height = size
        room_area = np.ones((width, height), dtype=bool)
        #  Convolve room_area into self.rooms, values of zero mean this room
        #  will fit.
        valid = scipy.signal.convolve(
            (self.rooms[..., floor] != 0).astype(int),
            room_area,
            "full",
        )[width - 1 : -width + 1, height - 1 : -height + 1]
        valid = np.transpose((valid == 0).nonzero())
        if not valid.size:
            msg = "No space left for room."
            raise NoRoomError(msg)
        x, y = self.rng.choice(valid)
        assert (self.rooms[x : x + width, y : y + height, floor] == 0).all()
        return slice(x, x + width), slice(y, y + height)

    def get_unclaimed_cell(self) -> tuple[int, int]:
        nz = self.get_unclaimed_cells().nonzero()
        i = self.rng.randint(0, len(nz[0]) - 1)
        return nz[0][i], nz[1][i]

    def get_unclaimed_cells(self) -> NDArray[np.bool_]:
        claimed = self.rooms > 0
        free = self.rooms == 0
        neighbors = scipy.signal.convolve(
            in1=claimed,
            in2=[
                [0, 1, 0],
                [1, 0, 1],
                [0, 1, 0],
            ],
            mode="same",
        )
        return (neighbors != 0) & free  # type: ignore[no-any-return]

    def finalize(self) -> None:  # noqa: C901
        def get_room_type(cx: int, cy: int, cz: int) -> RoomType:
            if 0 <= cx < self.rooms.shape[0] and 0 <= cy < self.rooms.shape[1]:
                return self.room_types[self.rooms[cx, cy, cz]]
            return self.room_types[-1]

        def iter_cells() -> Iterator[tuple[int, int, int]]:
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
            top_left_type = get_room_type(cx - 1, cy - 1, cz)

            left = cx * self.room_width
            top = cy * self.room_height
            right = left + self.room_width
            bottom = top + self.room_height

            left_tile = get_merge_tile(room_type, left_type)
            top_tile = get_merge_tile(room_type, top_type)
            top_left_tile = get_merge_tile(room_type, left_type, top_type, top_left_type)

            self.zone.data["tile"][left, top, cz] = top_left_tile
            self.zone.data["tile"][left + 1 : right, top, cz] = top_tile
            self.zone.data["tile"][left, top + 1 : bottom, cz] = left_tile
            self.zone.data["tile"][left + 1 : right, top + 1 : bottom, cz] = room_type.floor

        self.zone.data["room_id"] = -1
        self.zone.data["room_id"][:-1, :-1, :] = np.kron(self.rooms, np.ones((self.room_width, self.room_height, 1)))
        self.zone.room_types = self.room_types

        ShipRoomConnector(self).generate()

        for room_id, room in self.room_types.items():
            room.finalize(room_id, self)

    def show(self) -> str:
        def icon(x: int, y: int) -> str:
            if self.rooms[x, y] == -1:
                return " "
            return f"""{self.rooms[x, y, 0] % 10:i}"""

        return "\n".join("".join(icon(x, y) for x in range(self.length)) for y in range(self.width))
