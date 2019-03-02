from typing import Any

import engine.entity


class Null:
    def __new__(cls, *args: Any, **kargs: Any) -> None:
        return None


class Component:
    def on_added(self, entity: "engine.entity.Entity") -> None:
        pass

    def on_remove(self, entity: "engine.entity.Entity") -> None:
        pass
