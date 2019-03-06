
import obj.entity
import component.graphic
import component.item


class Item(obj.entity.Entity):
    class Graphic(component.graphic.Graphic):
        CH = ord("!")
        PRIORITY = -1

    class Item(component.item.Item):
        pass
