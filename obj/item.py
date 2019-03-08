from __future__ import annotations

import obj.entity
import component.graphic
import component.item


class BaseItem(obj.entity.Entity):
    class Graphic(component.graphic.Graphic):
        CH = ord("!")
        PRIORITY = -1

    class Item(component.item.Item):
        pass


class Item(BaseItem):
    pass


class SpareCore(BaseItem):
    class Graphic(BaseItem.Graphic):
        CH = ord("°")
        PRIORITY = -1

    class Item(BaseItem.Item):
        name = "spare drive core"
        tags = {"drive core"}
