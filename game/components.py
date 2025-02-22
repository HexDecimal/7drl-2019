"""Common components."""

from typing import Final

Name: Final = ("Name", str)
"""The name of an entity."""

MoveSpeed: Final = ("MoveSpeed", int)
AttackSpeed: Final = ("AttackSpeed", int)


MessageLog: Final = ("log", list[str])
"""Log of recorded messages."""
