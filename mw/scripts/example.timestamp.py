from mw.types import Timestamp

t = Timestamp('2009-02-13T23:31:30Z')

# Self casting
assert t == Timestamp(t)

# Unix timestamp (seconds since Jan. 1st 1970 GMT)
assert int(t) == 1234567890
assert t.unix() == 1234567890
assert t == Timestamp(1234567890)

# Database format %Y%m%d%H%M%S"
assert str(t) == "20090213233130"
assert t.short_format() == "20090213233130"
assert t == Timestamp("20090213233130")

# API format %Y-%m-%dT%H:%M:%SZ
assert t.long_format() == "2009-02-13T23:31:30Z"
assert t == Timestamp("2009-02-13T23:31:30Z")

# Simple math
assert Timestamp(2) - Timestamp(1) == 1


