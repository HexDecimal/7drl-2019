from __future__ import annotations

import tcod.ecs

from component.location import Location
from game.action import ActionResult, Impossible, Success
from game.action_logic import report
from game.components import Graphic, Interactable
from game.tags import IsBlocking, IsIn


def new_machine(world: tcod.ecs.Registry, location: Location) -> tcod.ecs.Entity:
    new_entity = world[object()]
    new_entity.components.update(
        {
            Location: location,
            Graphic: Graphic(ch=ord("#")),
        },
    )
    new_entity.tags.add(IsBlocking)
    return new_entity


def _get_core(entity: tcod.ecs.Entity) -> tcod.ecs.Entity | None:
    """Get a dive core held in an entities inventory."""
    for item in entity.world.Q.all_of(tags=["drive core"], relations=[(IsIn, entity)]):
        return item
    return None


def drive_core_interaction(issuer: tcod.ecs.Entity, target: tcod.ecs.Entity) -> ActionResult:
    """Interact with or install drive cores."""
    if not _get_core(issuer):
        return Impossible("Need core.")

    core = _get_core(issuer)
    assert core
    core.relation_tag[IsIn] = target
    report(issuer, "{You} install the core.")
    return Success()


def new_drive_core(world: tcod.ecs.Registry, location: Location) -> tcod.ecs.Entity:
    new_entity = new_machine(world, location)
    new_entity.components.update(
        {
            Graphic: Graphic(ch=ord("╪")),
            Interactable: drive_core_interaction,
        },
    )
    return new_entity
