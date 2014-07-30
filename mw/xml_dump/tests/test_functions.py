import os.path

from nose.tools import eq_, raises

from ..functions import open_file


def test_open_file_7z():
    f = open_file(os.path.join(os.path.dirname(__file__), "test.7z"))
    eq_(f.read(), b"foobartest\n")
