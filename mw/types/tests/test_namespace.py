from nose.tools import eq_

from ..namespace import Namespace


def test_namespace():
    namespace = Namespace(10, "Foo", canonical="Bar", aliases={'WT'}, case="foobar")

    eq_(namespace.id, 10)
    eq_(namespace.name, "Foo")
    eq_(namespace.canonical, "Bar")
    eq_(namespace.aliases, {'WT'})
    eq_(namespace.case, "foobar")
