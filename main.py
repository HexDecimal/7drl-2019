#!/usr/bin/env python3
from typing import Any, Dict

import tcod

import g
import state
import engine.world
import objects.living

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
        g.world = engine.world.World(100, 100)
        g.player = objects.living.Player(g.world[1, 1, 0])
        objects.living.TestActor(g.world[50, 1, 0])
        state.Game().activate()


if __name__ == "__main__":
    main()
