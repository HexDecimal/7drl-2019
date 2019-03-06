from __future__ import annotations

from typing import Any, Dict, Optional, TYPE_CHECKING

import component.base
if TYPE_CHECKING:
    import component.actor
    import component.character
    import component.container
    import component.graphic
    import component.item
    import component.location
    import component.verb


class Entity:
    location: component.location.Location
    actor: Optional[component.actor.Actor]
    character: Optional[component.character.Character]
    container: Optional[component.container.Container]
    graphic: Optional[component.graphic.Graphic]
    interactable: Optional[component.verb.Interactable]
    item: Optional[component.item.Item]

    def __init__(self, location: component.location.Location) -> None:
        self._components: Dict[str, component.base.Component] = {}
        self.location = location
        for attr in dir(self):
            if attr[0].isupper():
                setattr(self, attr.lower(), getattr(self, attr)())

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
