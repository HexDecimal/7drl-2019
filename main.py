#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Dict

import tcod

import g
import state
import engine.model

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
        g.model = engine.model.Model()
        state.Game().activate()


if __name__ == "__main__":
    main()
