from __future__ import annotations

from typing import TYPE_CHECKING

import tcod.path

import actions.base
import actions.common

if TYPE_CHECKING:
    import obj.entity


class MoveTo(actions.base.LocationAction):
    def poll(self) -> actions.base.Action | None:
        if not self.location.data["tile"]["walkable"]:
            return None
        for entity in self.location.contents:
            if entity.physicality and entity.physicality.blocking:
                return None
        return self

    def action(self) -> int:
        assert self.entity.physicality
        old_xyz = self.entity.location.xyz
        new_xyz = self.location.xyz
        self.entity.location = self.location
        if old_xyz[0] - new_xyz[0] and old_xyz[1] - new_xyz[1]:
            return self.entity.physicality.move_speed * 3 // 2
        return self.entity.physicality.move_speed


class MoveBy(actions.base.BumpAction):
    def poll(self) -> actions.base.Action | None:
        return MoveTo(self.entity, self.destination).poll()


class MoveTowards(actions.base.LocationAction):
    def poll(self) -> actions.base.Action | None:
        x = self.location.xyz[0] - self.entity.location.xyz[0]
        y = self.location.xyz[1] - self.entity.location.xyz[1]
        x //= abs(x)
        y //= abs(y)
        return MoveBy(self.entity, (x, y, 0))


class Follow(actions.base.EntityAction):
    def __init__(
        self,
        entity: obj.entity.Entity,
        target: obj.entity.Entity,
    ):
        super().__init__(entity, target)
        z = entity.location.xyz[2]
        self.pathfinder = tcod.path.AStar(
            entity.location.zone.data["tile"]["walkable"][:, :, z],
        )

    def poll(self) -> actions.base.Action | None:
        my_coord = self.entity.location.xyz[:2]
        target_coord = self.target.location.xyz[:2]
        path = self.pathfinder.get_path(*my_coord, *target_coord)
        if len(path) <= 1:
            return None
        return MoveTo(
            self.entity,
            self.zone[(*path[0], self.entity.location.xyz[2])],  # type: ignore
        ).poll()
