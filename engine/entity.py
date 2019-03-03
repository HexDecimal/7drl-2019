from typing import Any, Dict, Optional, TYPE_CHECKING

import engine.component
if TYPE_CHECKING:
    import engine.actor
    import engine.graphic
    import engine.location


class Entity:
    location: "engine.location.Location"
    Actor: Any = engine.component.Null
    actor: Optional["engine.actor.Actor"]
    Graphic: Any = engine.component.Null
    graphic: Optional["engine.graphic.Graphic"]

    def __init__(self, location: "engine.location.Location") -> None:
        self._components: Dict[str, engine.component.Component] = {}
        self.location = location
        for annotation in self.__class__.__annotations__:
            if annotation[0].isupper():
                setattr(self, annotation.lower(), getattr(self, annotation)())

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
