from typing import Tuple, Optional

import engine.component


class Graphic(engine.component.Component):
    CH = ord('!')
    FG = (255, 255, 255)

    def __init__(
        self,
        ch: Optional[int] = None,
        fg: Optional[Tuple[int, int, int]] = None,
    ):
        self.ch = ch if ch is not None else self.CH
        self.fg = fg if fg is not None else self.FG

    def get(self) -> Tuple[int, Tuple[int, int, int]]:
        return self.ch, self.fg
