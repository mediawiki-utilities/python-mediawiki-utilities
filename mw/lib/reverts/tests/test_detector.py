from nose.tools import eq_

from ..detector import Detector


def test_detector():
    detector = Detector(2)

    eq_(detector.process("a", {'id': 1}), None)

    # Check noop
    eq_(detector.process("a", {'id': 2}), None)

    # Short revert
    eq_(detector.process("b", {'id': 3}), None)
    eq_(
        detector.process("a", {'id': 4}),
        ({'id': 4}, [{'id': 3}], {'id': 2})
    )

    # Medium revert
    eq_(detector.process("c", {'id': 5}), None)
    eq_(detector.process("d", {'id': 6}), None)
    eq_(
        detector.process("a", {'id': 7}),
        ({'id': 7}, [{'id': 6}, {'id': 5}], {'id': 4})
    )

    # Long (undetected) revert
    eq_(detector.process("e", {'id': 8}), None)
    eq_(detector.process("f", {'id': 9}), None)
    eq_(detector.process("g", {'id': 10}), None)
    eq_(detector.process("a", {'id': 11}), None)
