from nose.tools import eq_
from ..peekable import Peekable


def test_peekable():
    iterable = range(0, 100)
    iterable = Peekable(iterable)
    expected = list(range(0, 100))

    result = []

    assert not iterable.empty()
    eq_(iterable.peek(), expected[0])
    result.append(next(iterable))

    eq_(iterable.peek(), expected[1])
    result.append(next(iterable))

    result.extend(list(iterable))
    eq_(result, expected)
