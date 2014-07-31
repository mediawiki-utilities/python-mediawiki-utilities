from nose.tools import eq_

from ..text import Text


def test_immutability():
    a = Text("foo")
    b = Text(a)
    eq_(id(a), id(b))


def test_empty_constructor():
    t = Text()
    eq_(t, "")
    eq_(t.deleted, False)
    eq_(t.id, None)
    eq_(t.xml_space, "preserve")
    eq_(t.bytes, None)


def test_deleted_constructor():
    t = Text("", deleted=True)
    eq_(t, "")
    eq_(t.deleted, True)
    eq_(t.id, None)
    eq_(t.xml_space, "preserve")
    eq_(t.bytes, None)


def test_full_constructor():
    t = Text("Foobar!", deleted=False, id=10, xml_space="foobar", bytes=1001)
    eq_(t, "Foobar!")
    eq_(t.deleted, False)
    eq_(t.id, 10)
    eq_(t.xml_space, "foobar")
    eq_(t.bytes, 1001)


def test_serialize():
    t = Text("Foobar!", deleted=False, id=10, xml_space="foobar", bytes=1001)
    t2 = Text.deserialize(t.serialize())
    eq_(t2.deleted, False)
    eq_(t2.id, 10)
    eq_(t2.xml_space, "foobar")
    eq_(t2.bytes, 1001)
