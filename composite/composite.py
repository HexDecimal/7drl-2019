from __future__ import annotations

from typing import Any, Dict, List, Sequence, Type, TypeVar

T = TypeVar("T")


class Composite:
    __slots__ = ("_components", "__weakref__")

    def __init__(self) -> None:
        self._components: Dict[Any, List[Any]] = {}

    def __getitem__(self, key: Type[T]) -> Sequence[T]:
        """Return all components derived from the `key` class."""
        return self._components.get(key, ())

    def __contains__(self, item: Any) -> bool:
        """Return True if `item` is in or is a class handled by self."""
        return item in self._components or item in self[item.__class__]

    def add(self, obj: Any) -> None:
        """Add a component to this composite object."""
        for cls in obj.__class__.__mro__:
            try:
                self._components[cls].append(obj)
            except KeyError:
                self._components[cls] = [obj]

    def remove(self, obj: Any) -> None:
        """Remove a component from this composite object."""
        for cls in obj.__class__.__mro__:
            self._components[cls].remove(obj)
            if not self._components[cls]:
                del self._components[cls]


__all__ = ("Composite",)
