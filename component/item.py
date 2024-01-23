from __future__ import annotations

import attrs


@attrs.define(frozen=True)
class Item:
    name: str = "item"
    weight: int = 1
    tags: frozenset[str] = frozenset()
