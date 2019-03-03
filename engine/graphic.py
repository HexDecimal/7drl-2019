from typing import Tuple

import engine.component


class Graphic(engine.component.Component):
    CH = ord('!')
    FG = (255, 255, 255)

    def get(self) -> Tuple[int, Tuple[int, int, int]]:
        return self.CH, self.FG
