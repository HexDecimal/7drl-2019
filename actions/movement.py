from __future__ import annotations

import attrs
import tcod.ecs
import tcod.path

import actions.base
import actions.common
from actions import ActionResult, Impossible, Success
from component.location import Location
from component.physicality import Physicality
from engine.helpers import active_zone


@attrs.define()
class MoveTo:
    location: Location

    def perform(self, actor: tcod.ecs.Entity) -> ActionResult:
        if not self.location.data["tile"]["walkable"]:
            return Impossible("Blocked.")
        for entity in actor.world.Q.all_of(tags=[self.location], components=[Physicality]):
            if entity.components[Physicality].blocking:
                return Impossible("Blocked.")

        old_xyz = actor.components[Location].xyz
        new_xyz = self.location.xyz
        actor.components[Location] = self.location
        if old_xyz[0] - new_xyz[0] and old_xyz[1] - new_xyz[1]:
            return Success(actor.components[Physicality].move_speed * 3 // 2)
        return Success(actor.components[Physicality].move_speed)


@attrs.define()
class MoveBy(actions.base.BumpAction):
    def perform(self, entity: tcod.ecs.Entity) -> ActionResult:
        return MoveTo(entity.components[Location] + self.direction).perform(entity)


@attrs.define()
class MoveTowards:
    location: Location

    def perform(self, entity: tcod.ecs.Entity) -> ActionResult:
        x = self.location.xyz[0] - entity.components[Location].xyz[0]
        y = self.location.xyz[1] - entity.components[Location].xyz[1]
        x //= abs(x)
        y //= abs(y)
        return MoveBy((x, y, 0)).perform(entity)


@attrs.define()
class Follow:
    target: tcod.ecs.Entity
    pathfinder: tcod.path.AStar | None = None

    def perform(self, entity: tcod.ecs.Entity) -> ActionResult:
        if self.pathfinder is None:
            z = entity.components[Location].z
            self.pathfinder = tcod.path.AStar(
                entity.components[Location].zone.data["tile"]["walkable"][:, :, z],
            )

        my_coord = entity.components[Location].xyz[:2]
        target_coord = self.target.components[Location].xyz[:2]
        path = self.pathfinder.get_path(*my_coord, *target_coord)
        if len(path) <= 1:
            return Impossible("Destination reached.")
        return MoveTo(
            active_zone()[(*path[0], entity.components[Location].xyz[2])],
        ).perform(entity)
