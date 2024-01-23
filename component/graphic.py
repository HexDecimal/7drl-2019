from __future__ import annotations

import attrs


@attrs.define(frozen=True)
class Graphic:
    ch: int = ord("!")
    fg: tuple[int, int, int] = (255, 255, 255)
    priority: int = 0

    def get(self) -> tuple[int, tuple[int, int, int]]:
        return self.ch, self.fg
