from typing import Any, Optional

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

    @property
    def world(self) -> "engine.world.World":
        assert self.entity
        return self.entity.location.world
