from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Any, Generic, Optional, TypeVar

import component.base
import composite
from component.actor import Actor
from component.container import Container
from component.graphic import Graphic
from component.item import Item
from component.location import Location
from component.physicality import Physicality

if TYPE_CHECKING:
    import component.actor
    import component.container
    import component.graphic
    import component.item
    import component.location
    import component.physicality
    import component.verb

T = TypeVar("T", bound="component.base.Component")


class Ensure(Generic[T]):
    __slots__ = ("attr",)

    attr: Any

    def __init__(self, attr: Any) -> None:
        self.attr = attr

    def __get__(self, obj: Entity, objtype: Any = None) -> T:
        assert len(obj[self.attr]) <= 1, obj[self.attr]
        return obj[self.attr][0]  # type: ignore

    def __set__(self, obj: Entity, value: Optional[T]) -> None:
        try:
            (old,) = obj[self.attr]
            assert len(obj[self.attr]) == 1, obj[self.attr]
            obj.remove(old)
            assert len(obj[self.attr]) == 0, obj[self.attr]
        except ValueError:
            pass
        if value is not None:
            obj.add(value)
            assert len(obj[self.attr]) == 1, obj[self.attr]


class Option(Ensure[T]):
    __slots__ = ()

    def __get__(  # type: ignore
        self,
        obj: Entity,
        objtype: Any = None,
    ) -> Optional[T]:
        try:
            return super().__get__(obj, objtype)
        except IndexError:
            return None


class Entity(composite.Composite):
    __slots__ = ()
    location: Ensure[Location] = Ensure(Location)
    actor: Option[Actor] = Option(Actor)
    container: Option[Container] = Option(Container)
    graphic: Option[Graphic] = Option(Graphic)
    physicality: Option[Physicality] = Option(Physicality)
    item: Option[Item] = Option(Item)

    def __init__(self, location: component.location.Location) -> None:
        super().__init__()
        self.add(location)
        for attr in dir(self):
            value = getattr(self, attr)
            if not inspect.isclass(value):
                continue
            if not issubclass(value, component.base.Component):
                continue
            self.add(value())

    def destroy(self) -> None:
        """Unlink this entity from the world."""
        for my_component in self[component.base.Component]:
            my_component.on_destroy(self)

    def is_alive(self) -> bool:
        """Return True if this entity has not been destroyed."""
        return self in self.location.contents

    def add(self, obj: Any) -> None:
        """Add a component to this composite object."""
        super().add(obj)
        obj.on_added(self)

    def remove(self, obj: Any) -> None:
        """Remove a component from this composite object."""
        obj.on_remove(self)
        super().remove(obj)
