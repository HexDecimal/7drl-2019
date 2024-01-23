from __future__ import annotations

import tcod.ecs
import tcod.path

import actions.base
import actions.common
from component.location import Location
from component.physicality import Physicality
from engine.helpers import active_zone


class MoveTo(actions.base.LocationAction):
    def poll(self) -> actions.base.Action | None:
        if not self.location.data["tile"]["walkable"]:
            return None
        for entity in self.entity.world.Q.all_of(tags=[self.location], components=[Physicality]):
            if entity.components[Physicality].blocking:
                return None
        return self

    def action(self) -> int:
        old_xyz = self.entity.components[Location].xyz
        new_xyz = self.location.xyz
        self.entity.components[Location] = self.location
        if old_xyz[0] - new_xyz[0] and old_xyz[1] - new_xyz[1]:
            return self.entity.components[Physicality].move_speed * 3 // 2
        return self.entity.components[Physicality].move_speed


class MoveBy(actions.base.BumpAction):
    def poll(self) -> actions.base.Action | None:
        return MoveTo(self.entity, self.destination).poll()


class MoveTowards(actions.base.LocationAction):
    def poll(self) -> actions.base.Action | None:
        x = self.location.xyz[0] - self.entity.components[Location].xyz[0]
        y = self.location.xyz[1] - self.entity.components[Location].xyz[1]
        x //= abs(x)
        y //= abs(y)
        return MoveBy(self.entity, (x, y, 0))


class Follow(actions.base.EntityAction):
    def __init__(
        self,
        entity: tcod.ecs.Entity,
        target: tcod.ecs.Entity,
    ) -> None:
        super().__init__(entity, target)
        z = entity.components[Location].z
        self.pathfinder = tcod.path.AStar(
            entity.components[Location].zone.data["tile"]["walkable"][:, :, z],
        )

    def poll(self) -> actions.base.Action | None:
        my_coord = self.entity.components[Location].xyz[:2]
        target_coord = self.target.components[Location].xyz[:2]
        path = self.pathfinder.get_path(*my_coord, *target_coord)
        if len(path) <= 1:
            return None
        return MoveTo(
            self.entity,
            active_zone()[(*path[0], self.entity.components[Location].xyz[2])],
        ).poll()
