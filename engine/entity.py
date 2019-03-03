from typing import Any, Dict, Optional

import engine.actor
import engine.component
import engine.location


class Entity:
    Actor: Any = engine.component.Null
    actor: Optional[engine.actor.Actor]
    location: engine.location.Location

    def __init__(self, location: engine.location.Location) -> None:
        self._components: Dict[str, engine.component.Component] = {}
        self.location = location
        self.actor = self.Actor()

    def destroy(self) -> None:
        """Unlink this entity from the world."""
        self.actor = None
        self.location.contents.remove(self)

    def __setattr__(
        self,
        attr: str,
        value: Optional[engine.component.Component],
    ) -> None:
        if attr.startswith("_"):  # No special action for private attributes.
            return super().__setattr__(attr, value)
        old: Any = self._components.get(attr, None)
        if old and value:
            self._components[attr] = value
            value.on_replace(self, old)
        elif old:
            del self._components[attr]
            old.on_remove(self)
        elif value:
            self._components[attr] = value
            value.on_added(self)

    def __getattr__(self, attr: str) -> Any:
        try:
            return self._components[attr]
        except KeyError:
            return None


class Player(Entity):
    class Actor(engine.actor.Player):
        pass
