from nose.tools import eq_

from .. import ordered


def test_circle():
    circle = ordered.Circle(3)

    eq_(0, len(circle))
    print(circle.state())
    eq_(None, circle.append(5))
    eq_(1, len(circle))
    print(circle.state())
    eq_(None, circle.append(6))
    eq_(2, len(circle))
    print(circle.state())
    eq_(None, circle.append(7))
    eq_(3, len(circle))
    print(circle.state())
    eq_(5, circle.append(8))
    eq_(3, len(circle))
    print(circle.state())

    eq_([6, 7, 8], list(circle))

    print(circle.state())
    eq_([8, 7, 6], list(reversed(circle)))


def test_historical_map():
    hist = ordered.HistoricalMap(maxlen=2)

    assert "foo" not in hist

    eq_(None, hist.insert('foo', "bar1"))

    assert "foo" in hist

    eq_(None, hist.insert('foo', "bar2"))

    eq_(('foo', "bar1"), hist.insert('not_foo', "not_bar"))
