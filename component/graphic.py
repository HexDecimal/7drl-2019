from __future__ import annotations

import component.base


class Graphic(component.base.Component):
    CH = ord("!")
    FG = (255, 255, 255)
    PRIORITY = 0

    def __init__(
        self,
        ch: int | None = None,
        fg: tuple[int, int, int] | None = None,
        priority: int | None = None,
    ) -> None:
        self.ch = ch if ch is not None else self.CH
        self.fg = fg if fg is not None else self.FG
        self.priority = priority if priority is not None else self.PRIORITY

    def get(self) -> tuple[int, tuple[int, int, int]]:
        return self.ch, self.fg
