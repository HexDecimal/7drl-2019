import tcod

import g
import state
import engine.world
import engine.entity

FONT = {
    "fontFile": "terminal8x12_gs_ro.png",
    "flags": tcod.FONT_LAYOUT_CP437,  # type: ignore
}

CONFIG = {
    "w": 800 // 8,
    "h": 500 // 12,
    "title": None,
    "order": "F",
}


def main() -> None:
    tcod.console_set_custom_font(**FONT)  # type: ignore
    with tcod.console_init_root(**CONFIG) as g.console:  # type: ignore
        g.world = engine.world.World(100, 100)
        engine.entity.Player(g.world[0, 0, 0])
        state.Game().activate()


if __name__ == "__main__":
    main()
