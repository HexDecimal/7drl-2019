from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import engine.entity
    import engine.world


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

    @property
    def world(self) -> "engine.world.World":
        assert self.entity
        return self.entity.location.world
