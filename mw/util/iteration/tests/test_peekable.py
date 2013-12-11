from nose.tools import eq_
from ..peekable import peekable

def test_peekable():
	iterable = xrange(0,100)
	iterable = peekable(iterable)
	expected = range(0, 100)
	
	result = []
	
	assert not iterable.empty()
	eq_(iterable.peek(), expected[0])
	result.append(iterable.next())
	
	eq_(iterable.peek(), expected[1])
	result.append(iterable.next())
	
	result.extend(list(iterable))
	eq_(result, expected)
	
	
