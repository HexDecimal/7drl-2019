#!/usr/bin/env python3
"""Main script."""

from __future__ import annotations

from typing import Any

import tcod.console
import tcod.context
import tcod.tileset

import g
import game.state
import game.state_logic
import game.states
import game.world_init

CONFIG: dict[str, Any] = {
    "width": 800,
    "height": 500,
    "title": None,
    "tileset": tcod.tileset.load_tilesheet("assets/terminal8x12_gs_ro.png", 16, 16, tcod.tileset.CHARMAP_CP437),
    "vsync": True,
}

g.console = tcod.console.Console(CONFIG["width"] // 8, CONFIG["height"] // 12, order="F")


def main() -> None:
    """Main entry function."""
    with tcod.context.new(**CONFIG) as g.context:
        g.world = game.world_init.new_world()
        game.state_logic.handle_result(game.state.Rebase(game.states.InGame()))
        game.state_logic.loop()


if __name__ == "__main__":
    main()
