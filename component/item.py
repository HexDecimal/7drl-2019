from __future__ import annotations

from typing import Set

from component.base import Component


class Item(Component):
    name = "item"
    weight = 1
    tags: Set[str] = set()
