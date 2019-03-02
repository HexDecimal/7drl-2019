import tcod

import g
import state

FONT = {
    "fontFile": "terminal8x12_gs_ro.png",
    "flags": tcod.FONT_LAYOUT_CP437,
}

CONFIG = {
    "w": 800 // 8,
    "h": 500 // 12,
    "title": None,
    "order": "F",
}


def main() -> None:
    tcod.console_set_custom_font(**FONT)
    with tcod.console_init_root(**CONFIG) as g.console:
        state.MainMenu().activate()


if __name__ == "__main__":
    main()
