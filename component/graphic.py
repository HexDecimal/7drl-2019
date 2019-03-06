from __future__ import annotations

from typing import Tuple, Optional

import component.base


class Graphic(component.base.Component):
    CH = ord('!')
    FG = (255, 255, 255)
    PRIORITY = 0

    def __init__(
        self,
        ch: Optional[int] = None,
        fg: Optional[Tuple[int, int, int]] = None,
        priority: Optional[int] = None,
    ):
        self.ch = ch if ch is not None else self.CH
        self.fg = fg if fg is not None else self.FG
        self.priority = priority if priority is not None else self.PRIORITY

    def get(self) -> Tuple[int, Tuple[int, int, int]]:
        return self.ch, self.fg
