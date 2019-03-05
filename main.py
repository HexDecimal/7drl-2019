#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Dict

import tcod

import g
import state
import obj.living
import procgen.shipgen

FONT: Dict[str, Any] = {
    "fontFile": "terminal8x12_gs_ro.png",
    "flags": tcod.FONT_LAYOUT_CP437,
}

CONFIG: Dict[str, Any] = {
    "w": 800 // 8,
    "h": 500 // 12,
    "title": None,
    "order": "F",
}


def main() -> None:
    tcod.console_set_custom_font(**FONT)
    with tcod.console_init_root(**CONFIG) as g.console:
        ship = procgen.shipgen.Ship()
        g.zone = ship.zone
        g.player = obj.living.Player(g.zone[ship.start_position])
        obj.living.TestRobot(g.player.location.get_relative(2, 2, 0))
        del ship
        state.Game().activate()


if __name__ == "__main__":
    main()
