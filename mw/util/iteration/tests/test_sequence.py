from nose.tools import eq_
from ..sequence import sequence


def test_sequence():
    foo = [{'val': 3}, {'val': 5}]
    bar = [{'val': 1}, {'val': 10}, {'val': 15}]
    expected = [{'val': 1}, {'val': 3}, {'val': 5}, {'val': 10}, {'val': 15}]

    result = list(sequence(foo, bar, compare=lambda i1, i2: i1['val'] < i2['val']))
    eq_(expected, result)
