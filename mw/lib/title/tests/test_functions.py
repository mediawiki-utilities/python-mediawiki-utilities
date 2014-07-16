from nose.tools import eq_

from ..functions import normalize


def test_normalize():
    eq_("Foobar", normalize("Foobar"))  # Same
    eq_("Foobar", normalize("foobar"))  # Capitalize
    eq_("FooBar", normalize("fooBar"))  # Late capital
    eq_("Foo_bar", normalize("Foo bar"))  # Space
