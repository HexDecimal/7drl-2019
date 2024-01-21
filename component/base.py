from __future__ import annotations

from typing import TYPE_CHECKING, Any

import g

if TYPE_CHECKING:
    import engine.model
    import engine.zone
    import obj.entity


class Null:
    def __new__(cls, *args: Any, **kargs: Any) -> None:  # type: ignore[misc]
        return None


class Component:
    def on_added(self, entity: obj.entity.Entity) -> None:
        pass

    def on_remove(self, entity: obj.entity.Entity) -> None:
        pass

    def on_destroy(self, entity: obj.entity.Entity) -> None:
        """Owner entity is being destructed."""

    @property
    def model(self) -> engine.model.Model:
        return g.model


class OwnedComponent(Component):
    owner: obj.entity.Entity

    def on_added(self, entity: obj.entity.Entity) -> None:
        self.owner = entity
        super().on_added(entity)

    @property
    def zone(self) -> engine.zone.Zone:
        return self.owner.location.zone
