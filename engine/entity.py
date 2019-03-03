from typing import Any, Dict, Optional

import engine.actor
import engine.component
import engine.location


class Entity:
    Actor: Any = engine.component.Null
    actor: Optional[engine.actor.Actor]

    def __init__(self, location: engine.location.Location) -> None:
        self._location = location
        self._components: Dict[str, engine.component.Component] = {}
        location.contents.append(self)
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
        if attr == "location":
            return super().__setattr__(attr, value)
        if attr in self._components:
            self._components[attr].on_remove(self)
            del self._components[attr]
        if value:
            self._components[attr] = value
            value.on_added(self)

    def __getattr__(self, attr: str) -> Any:
        try:
            return self._components[attr]
        except KeyError:
            return None

    @property
    def location(self) -> engine.location.Location:
        """Return the current location."""
        return self._location

    @location.setter
    def location(self, value: engine.location.Location) -> None:
        """Change location, moving this entity to the new location contents.
        """
        if self._location is value:
            return
        assert self not in value.contents
        assert self._location.world is value.world
        self._location.contents.remove(self)
        self._location = value
        value.contents.append(self)


class Player(Entity):
    class Actor(engine.actor.Player):
        pass
