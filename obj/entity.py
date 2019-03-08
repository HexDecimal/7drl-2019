from __future__ import annotations

from typing import Any, Dict, Generic, Optional, TypeVar, TYPE_CHECKING

import component.base
if TYPE_CHECKING:
    import component.actor
    import component.base
    import component.container
    import component.graphic
    import component.item
    import component.location
    import component.physicality
    import component.verb

T = TypeVar("T", bound="component.base.Component")


class Ensure(Generic[T]):
    __slots__ = "attr",

    def __init__(self, attr: str):
        self.attr = attr

    def __get__(self, obj: Entity, objtype: Any = None) -> T:
        return obj._components[self.attr]  # type: ignore

    def __set__(self, obj: Entity, value: T) -> None:
        old: Optional[T] = obj._components.get(self.attr, None)  # type: ignore
        if old is not None:
            obj._components[self.attr] = value
            value.on_replace(obj, old)
        else:
            obj._components[self.attr] = value
            value.on_added(obj)


class Option(Ensure[T]):
    __slots__ = ()

    def __get__(  # type: ignore
        self, obj: Entity, objtype: Any = None,
    ) -> Optional[T]:
        try:
            return super().__get__(obj, objtype)
        except KeyError:
            return None

    def __set__(self, obj: Entity, value: Optional[T]) -> None:
        if value is not None:
            return super().__set__(obj, value)

        old: Optional[T] = obj._components.get(self.attr, None)  # type: ignore
        del obj._components[self.attr]
        if old is not None:
            old.on_remove(obj)


class Entity:
    __slots__ = "_components",
    location: Ensure[component.location.Location] = Ensure("location")
    actor: Option[component.actor.Actor] = Option("actor")
    container: Option[component.container.Container] = Option("container")
    graphic: Option[component.graphic.Graphic] = Option("graphic")
    physicality: Option[component.physicality.Physicality] = \
        Option("physicality")
    interactable: Option[component.verb.Interactable] = Option("interactable")
    item: Option[component.item.Item] = Option("item")

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
