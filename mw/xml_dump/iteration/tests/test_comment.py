from nose.tools import eq_

from ..comment import Comment


def test_immutability():
    c = Comment("foo")
    b = Comment(c)
    eq_(id(c), id(b))


def test_empty_constructor():
    c = Comment()
    eq_(c, "")
    eq_(c.deleted, False)


def test_deleted_constructor():
    c = Comment("", deleted=True)
    eq_(c, "")
    eq_(c.deleted, True)


def test_full_constructor():
    c = Comment("Foobar!", deleted=False)
    eq_(c, "Foobar!")
    eq_(c.deleted, False)


def test_serialize():
    c = Comment("Foobar!", deleted=False)
    c2 = Comment.deserialize(c.serialize())
    eq_(c2.deleted, False)
