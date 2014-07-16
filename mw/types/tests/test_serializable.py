from nose.tools import eq_

from .. import serializable


def test_type():
    class Foo(serializable.Type):
        def __init__(self, foo, bar):
            self.foo = foo
            self.bar = bar

    foo = Foo(1, "bar")
    eq_(foo, Foo.deserialize(foo))
    eq_(foo, Foo.deserialize(foo.serialize()))


def test_dict():
    d = serializable.Dict()
    d['foo'] = "bar"
    d['derp'] = "herp"

    eq_(d['foo'], "bar")
    assert 'derp' in d

    eq_(d, serializable.Dict.deserialize(d.serialize(), str))
