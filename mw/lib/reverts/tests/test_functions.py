from nose.tools import eq_

from ..functions import reverts


def test_reverts():
    checksum_revisions = [
        ("a", {'id': 1}),
        ("b", {'id': 2}),
        ("c", {'id': 3}),
        ("a", {'id': 4}),
        ("d", {'id': 5}),
        ("b", {'id': 6}),
        ("a", {'id': 7})
    ]

    expected = [
        ({'id': 4}, [{'id': 3}, {'id': 2}], {'id': 1}),
        ({'id': 7}, [{'id': 6}, {'id': 5}], {'id': 4})
    ]

    for revert in reverts(checksum_revisions, radius=2):
        eq_(revert, expected.pop(0))
