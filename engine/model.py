from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING

import procgen.shipgen
import obj.living
import obj.item
if TYPE_CHECKING:
    import engine.zone
    import obj.entity


class Model:
    zone: engine.zone.Zone  # The active zone.
    player: obj.entity.Entity  # The primary player entity.
    log: List[str]

    def __init__(self) -> None:
        ship = procgen.shipgen.Ship()
        self.zone = ship.zone
        self.player = obj.living.Player(self.zone[ship.start_position])
        obj.living.TestRobot(self.player.location.get_relative(2, 2, 0))
        obj.item.Item(self.player.location.get_relative(1, 1, 0))
        self.log = []

    @property
    def controlled(self) -> Optional[obj.entity.Entity]:
        """The active player controlled entity,"""
        return self.zone.player
