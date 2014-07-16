from nose.tools import eq_

from .. import difference


def test_sequence_matcher():
    t1 = "foobar derp hepl derpl"
    t2 = "fooasldal 3 hepl asl a derpl"

    ops = difference.sequence_matcher(t1, t2)

    eq_("".join(difference.apply(ops, t1, t2)), t2)
