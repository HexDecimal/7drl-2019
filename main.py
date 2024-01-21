#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Dict

import tcod.tileset
import tcod.console
import tcod.context

import g
import state
import engine.model

CONFIG: Dict[str, Any] = {
    "width": 800,
    "height": 500,
    "title": None,
    "tileset": tcod.tileset.load_tilesheet("terminal8x12_gs_ro.png", 16, 16, tcod.tileset.CHARMAP_CP437),
    "vsync": True,
}

g.console = tcod.console.Console(CONFIG["width"] // 8, CONFIG["height"] // 12, order="F")

def main() -> None:
    with tcod.context.new(**CONFIG) as g.context:
        g.context
        g.model = engine.model.Model()
        state.Game().activate()


if __name__ == "__main__":
    main()
