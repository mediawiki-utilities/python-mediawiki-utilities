from nose.tools import eq_

from ..timestamp import Timestamp, LONG_MW_TIME_STRING

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
	
	
def test_strptime():
	eq_(
		Timestamp("2009-02-13T23:31:30Z"),
		Timestamp.strptime("2009-02-13T23:31:30Z", LONG_MW_TIME_STRING)
	)
	
	eq_(
		Timestamp.strptime(
			"expires 03:20, 21 November 2013 (UTC)",
			"expires %H:%M, %d %B %Y (UTC)"
		),
		Timestamp("2013-11-21T03:20:00Z")
	)
	
def test_strftime():
	eq_(
		Timestamp("2009-02-13T23:31:30Z").strftime(LONG_MW_TIME_STRING),
		"2009-02-13T23:31:30Z"
	)
	
	eq_(
		Timestamp("2009-02-13T23:31:30Z").strftime("expires %H:%M, %d %B %Y (UTC)"),
		"expires 23:31, 13 February 2009 (UTC)"
	)

def test_serialization():
	timestamp = Timestamp(1234567890)
	eq_(
		timestamp,
		Timestamp.deserialize(timestamp.serialize())
	)
