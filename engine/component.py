from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import engine.entity
    import engine.zone


class Null:
    def __new__(cls, *args: Any, **kargs: Any) -> None:
        return None


class Component:
    entity: Optional["engine.entity.Entity"] = None

    def on_added(self, entity: "engine.entity.Entity") -> None:
        pass

    def on_remove(self, entity: "engine.entity.Entity") -> None:
        pass

    def on_replace(self, entity: "engine.entity.Entity", old: Any) -> None:
        """Called instead of added/remove when an existing component is
        replaced."""
        old.on_remove(entity)
        self.on_added(entity)

    def on_destroy(self, entity: "engine.entity.Entity") -> None:
        """Owner entity is being destructed."""

    @property
    def zone(self) -> "engine.zone.Zone":
        assert self.entity
        return self.entity.location.zone
