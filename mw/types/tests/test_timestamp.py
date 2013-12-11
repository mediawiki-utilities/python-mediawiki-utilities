from nose.tools import eq_

from ..timestamp import Timestamp

def test_self():
	t1 = Timestamp(1234567890)
	
	# Unix timestamp
	eq_(t1, Timestamp(int(t1)))
	
	# Short format
	eq_(t1, Timestamp(t1.short_format()))
	
	# Long format
	eq_(t1, Timestamp(t1.long_format()))
	

def test_comparison():
	t1 = Timestamp(1234567890)
	t2 = Timestamp(1234567891)
	
	assert t1 < t2, "Less than comparison failed"
	assert t2 > t1, "Greater than comparison failed"

def test_subtraction():
	t1 = Timestamp(1234567890)
	t2 = Timestamp(1234567891)
	
	eq_(t2 - t1, 1)
	eq_(t1 - t2, -1)
	
	
