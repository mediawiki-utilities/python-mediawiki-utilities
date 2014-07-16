from nose.tools import eq_

from ..heap import Heap


def test_heap():
    h = Heap([5, 4, 7, 8, 2])
    eq_(h.pop(), 2)
    eq_(h.pop(), 4)
    eq_(h.pop(), 5)
    eq_(h.pop(), 7)
    eq_(h.pop(), 8)
    eq_(len(h), 0)

    h = Heap([10, 20, 100])
    eq_(h.pop(), 10)
    h.push(30)
    eq_(len(h), 3)
    eq_(h.pop(), 20)
    eq_(h.pop(), 30)
    eq_(h.pop(), 100)
    eq_(len(h), 0)

    h = Heap([(1, 7), (2, 4), (10, -100)])
    eq_(h.peek(), (1, 7))
    h.pop()
    eq_(h.pop(), (2, 4))
    eq_(h.pop(), (10, -100))
