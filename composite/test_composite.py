from . import Composite


def test_composite() -> None:
    comp = Composite()
    comp.add(1)
    assert 1 in comp
    assert int in comp
    assert comp[int][0] == 1
    assert comp[object][0] == 1
    comp.add(2)
    comp.remove(2)
    comp.remove(1)
    assert int not in comp
