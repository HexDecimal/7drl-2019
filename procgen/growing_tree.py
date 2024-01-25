from __future__ import annotations

from collections.abc import Iterable
from typing import Generic, TypeVar

T = TypeVar("T")


class AbstractGrowingTree(Generic[T]):
    """An abstract implementation of the growing tree algorithm.

    A sub-class needs to keep track of node neighbors and visited nodes.
    """

    def __init__(self, stem: Iterable[T] | None = None) -> None:
        """Initialize the stem."""
        self.stem: list[T] = list(stem) if stem is not None else []

    def generate(self) -> None:
        """Run the growing tree algorithm until the stem is exhausted."""
        while self.stem:
            self.grow()

    def grow(self) -> None:
        """Run a single step of the growing tree algorithm."""
        assert self.stem
        stem_index = self.select_stem()
        stem_node = self.stem[stem_index]
        neighbor = self.select_neighbor(stem_node)
        if neighbor:
            self.visit(neighbor, stem_node)
        else:
            self.stem.pop(stem_index)
            self.decay(stem_node)

    def visit(
        self,
        node: T,
        prev: T | None,
    ) -> None:
        """Mark a node as visited and extend the stem.

        This function should be overridden to add side effects.
        """
        self.stem.append(node)

    def decay(self, node: T) -> None:
        """The stem at `node` has no more unvisited neighbors.

        This function can be extended to add side effects.
        """

    def select_stem(self) -> int:
        """Return the index of the stem to grow from.

        This function should be overridden to set the behavior
        """
        raise NotImplementedError()

    def select_neighbor(
        self,
        node: T,
    ) -> T | None:
        """Return an unvisited neighbor to `node` if one exists.

        This function should be overridden to set the behavior
        """
        raise NotImplementedError()
