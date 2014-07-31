from nose.tools import eq_
from ..aggregate import aggregate


def test_group():
    l = [0, 1, 2, 3, 4, 5, 10, 11, 12, 13, 14]
    expected = [[0, 1, 2, 3, 4, 5], [10, 11, 12, 13, 14]]

    result = []
    for identifier, group in aggregate(l, lambda item: int(item / 10)):
        result.append(list(group))

    eq_(result, expected)
