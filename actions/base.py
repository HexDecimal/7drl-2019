from __future__ import annotations

import attrs

from actions import Action


@attrs.define()
class BumpAction(Action):
    """An action with a direction."""

    direction: tuple[int, int, int]
