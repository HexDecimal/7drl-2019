"""Collection of actions."""

from __future__ import annotations

from collections.abc import Iterator

import attrs
import tcod.ecs
import tcod.path

import component.actor
from component.location import Location
from engine.helpers import active_player
from game.action import Action, ActionResult, Impossible, Success
from game.action_logic import report
from game.components import AttackSpeed, Graphic, Interactable, MoveSpeed, Name
from game.tags import IsBlocking, IsControllable, IsControlled, IsIn, IsItem


@attrs.define()
class BumpAction(Action):
    """An action with a direction."""

    direction: tuple[int, int, int]


@attrs.define()
class FightPlayer:
    """Seek and attack player."""

    def __call__(self, entity: tcod.ecs.Entity) -> ActionResult:  # noqa: D102
        action = Follow(active_player()).__call__(entity)
        if action:
            return action
        return Attack(active_player()).__call__(entity)


def wait(_entity: tcod.ecs.Entity) -> ActionResult:
    """Idle action."""
    return Success()


@attrs.define()
class Interact:
    """Contextual interaction with contextual object."""

    target: tcod.ecs.Entity

    def __call__(self, entity: tcod.ecs.Entity) -> ActionResult:
        if Interactable in self.target.components:
            return self.target.components[Interactable].__call__(entity, self.target)
        return Impossible("Not interactable.")


@attrs.define()
class BumpInteract(BumpAction):
    """Contextual interaction in direction with contextual object."""

    def __call__(self, entity: tcod.ecs.Entity) -> ActionResult:
        destination = entity.components[Location] + self.direction
        for target in entity.world.Q.all_of(tags=[destination], components=[Interactable]):
            return Interact(target).__call__(entity)
        return Impossible("No target.")


@attrs.define()
class Bump:
    """Contextual interaction in direction."""

    direction: tuple[int, int, int]

    def __call__(self, entity: tcod.ecs.Entity) -> ActionResult:
        return (
            MoveBy(self.direction).__call__(entity)
            or BumpInteract(self.direction).__call__(entity)
            or BumpAttack(self.direction).__call__(entity)
        )


@attrs.define()
class PlayerControl:
    """Give immediate user control to this entity."""

    def __call__(self, entity: tcod.ecs.Entity) -> ActionResult:
        entity.tags.add(IsControllable)
        entity.tags.add(IsControlled)
        entity.components[Location].zone.camera = entity.components[Location].xyz
        return Impossible("End of action.")  # Further actions will be pending.


@attrs.define()
class Standby:
    """Idle action."""

    def __call__(self, _entity: tcod.ecs.Entity) -> ActionResult:
        return Impossible("End of action.")


@attrs.define()
class Attack:
    """Melee attack."""

    target: tcod.ecs.Entity

    def __call__(self, entity: tcod.ecs.Entity) -> ActionResult:
        if not entity.components[Location].is_adjacent(self.target.components[Location]):
            return Impossible("")

        del self.target.components[component.actor.Actor]
        self.target.components[Graphic] = Graphic(ord("%"), (63, 63, 63))
        return Success(entity.components.get(AttackSpeed, 100))


@attrs.define()
class BumpAttack(BumpAction):
    """Directional attack."""

    def __call__(self, entity: tcod.ecs.Entity) -> ActionResult:
        destination = entity.components[Location] + self.direction
        for target in entity.world.Q.all_of(tags=[destination], components=[component.actor.Actor]):
            return Attack(target).__call__(entity)
        return Impossible("Nothing to attack.")


@attrs.define()
class PickupItem:
    """Take an item off the floor."""

    target: tcod.ecs.Entity

    def __call__(self, entity: tcod.ecs.Entity) -> ActionResult:
        if IsItem not in self.target.tags:
            return Impossible("Not an item.")

        del self.target.components[Location]
        self.target.relation_tag[IsIn] = entity
        report(entity, "{You} pick up the {item}.", item=self.target.components.get(Name, "???"))
        return Success()


@attrs.define()
class PickupGeneral:
    """Contextual pickup action."""

    def get_items(self, entity: tcod.ecs.Entity) -> Iterator[ActionResult]:
        loc = entity.components[Location]
        for target in entity.world.Q.all_of(tags=[loc, IsItem]):
            action = PickupItem(target).__call__(entity)
            if action:
                yield action

    def __call__(self, entity: tcod.ecs.Entity) -> ActionResult:
        actions = list(self.get_items(entity))
        if actions:
            return actions[0]
        return Impossible("No items on floor.")


@attrs.define()
class MoveTo:
    """Teleport to position."""

    location: Location

    def __call__(self, actor: tcod.ecs.Entity) -> ActionResult:
        if not self.location.data["tile"]["walkable"]:
            return Impossible("Blocked.")
        for entity in actor.world.Q.all_of(tags=[self.location, IsBlocking]):
            if IsBlocking in entity.tags:
                return Impossible("Blocked.")

        old_xyz = actor.components[Location].xyz
        new_xyz = self.location.xyz
        actor.components[Location] = self.location
        if old_xyz[0] - new_xyz[0] and old_xyz[1] - new_xyz[1]:
            return Success(actor.components.get(MoveSpeed, 100) * 3 // 2)
        return Success(actor.components.get(MoveSpeed, 100))


@attrs.define()
class MoveBy(BumpAction):
    """Move in direction."""

    def __call__(self, entity: tcod.ecs.Entity) -> ActionResult:
        return MoveTo(entity.components[Location] + self.direction).__call__(entity)


@attrs.define()
class MoveTowards:
    """Dumb move towards action."""

    location: Location

    def __call__(self, entity: tcod.ecs.Entity) -> ActionResult:
        x = self.location.xyz[0] - entity.components[Location].xyz[0]
        y = self.location.xyz[1] - entity.components[Location].xyz[1]
        x //= abs(x)
        y //= abs(y)
        return MoveBy((x, y, 0)).__call__(entity)


@attrs.define()
class Follow:
    """Path to entity."""

    target: tcod.ecs.Entity
    pathfinder: tcod.path.AStar | None = None

    def __call__(self, entity: tcod.ecs.Entity) -> ActionResult:
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
        next_x, next_y = path[0]
        return MoveTo(
            entity.components[Location].replace(x=next_x, y=next_y),
        ).__call__(entity)


@attrs.define()
class ReturnControlToPlayer:
    """Abort remote control."""

    def __call__(self, entity: tcod.ecs.Entity) -> ActionResult:
        player = active_player()
        if entity is player:
            return Impossible("Already player.")
        entity.tags.discard(IsControllable)
        component.actor.Actor.take_control(player)
        report(entity, "{You} stop controlling the robot.")
        return Success(time_cost=0)


@attrs.define()
class RemoteControl:
    """Pass player control to entity.."""

    target: tcod.ecs.Entity

    def __call__(self, entity: tcod.ecs.Entity) -> ActionResult:
        if self.target is active_player():
            return ReturnControlToPlayer().__call__(entity)
        entity.tags.discard(IsControllable)
        component.actor.Actor.take_control(self.target)
        report(entity, "{You} begin controlling the robot remotely.")
        return Success(time_cost=0)
