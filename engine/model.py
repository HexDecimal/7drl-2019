from __future__ import annotations

from typing import TYPE_CHECKING

import obj.item
import obj.living
import obj.monster
import obj.robot
import procgen.shipgen

if TYPE_CHECKING:
    import engine.zone
    import obj.entity


class Model:
    zone: engine.zone.Zone  # The active zone.
    player: obj.entity.Entity  # The primary player entity.
    log: list[str]

    def __init__(self) -> None:
        ship = procgen.shipgen.Ship(1)
        self.zone = ship.zone
        self.player = ship.player
        self.log = []

    @property
    def controlled(self) -> obj.entity.Entity | None:
        """The active player controlled entity,"""
        return self.zone.player
