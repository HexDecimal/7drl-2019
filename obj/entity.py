from __future__ import annotations

from typing import Any, Dict, Optional, TYPE_CHECKING

import component.base
if TYPE_CHECKING:
    import component.actor
    import component.graphic
    import component.location
    import component.verb


class Entity:
    location: component.location.Location
    Actor: Any = component.base.Null
    actor: Optional[component.actor.Actor]
    Graphic: Any = component.base.Null
    graphic: Optional[component.graphic.Graphic]
    Interactable: Any = component.base.Null
    interactable: Optional[component.verb.Interactable]

    def __init__(self, location: component.location.Location) -> None:
        self._components: Dict[str, component.base.Component] = {}
        self.location = location
        for annotation in self.__class__.__annotations__:
            if annotation[0].isupper():
                setattr(self, annotation.lower(), getattr(self, annotation)())

    def destroy(self) -> None:
        """Unlink this entity from the world."""
        for my_component in list(self._components.values()):
            my_component.on_destroy(self)

    def is_alive(self) -> bool:
        """Return True if this entity has not been destroyed."""
        return self in self.location.contents

    def __setattr__(
        self,
        attr: str,
        value: Optional[component.base.Component],
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
