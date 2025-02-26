"""Common tags."""

from typing import Final

IsItem: Final = "IsItem"
"""Entity can be picked up and held."""

IsIn: Final = "IsIn"
"""Entity containment relation tag."""

IsBlocking: Final = "IsBlocking"
"""Entity is physically blocking."""

IsControllable: Final = "IsControllable"
"""Entity is player controlled on its turn."""

IsControlled: Final = "IsControlled"
"""Entity is currently being controlled."""

IsActive: Final = "IsActive"
"""Entity is active."""
