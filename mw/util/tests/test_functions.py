from nose.tools import eq_

from ..functions import none_or

def test_none_or():
	eq_(10, none_or("10", int))
	eq_(10.75, none_or("10.75", int))
	eq_(None, none_or(None, int))
	assert none_or("", int) != None
	assert none_or([], int) != None
	assert none_or({}, int) != None
	assert none_or(0, int) != None
	assert none_or(-1, int) != None
