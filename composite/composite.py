from __future__ import annotations

from collections.abc import Sequence
from typing import Any, TypeVar

T = TypeVar("T")


class Composite:
    __slots__ = ("_components", "__weakref__")

    def __init__(self) -> None:
        self._components: dict[Any, list[Any]] = {}

    def __getitem__(self, key: type[T]) -> Sequence[T]:
        """Return all components derived from the `key` class."""
        try:
            return self._components[key]
        except KeyError:
            return ()

    def __setitem__(self, key: type[T], value: T) -> None:
        """Replace all components of type `key` with just `value`."""
        if key not in value.__class__.__mro__:
            raise TypeError(f"{value} isn't an instance of {key}.")
        for component in list(self[key]):
            self.remove(component)
        self.add(value)

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


__all__ = ("Composite",)
