"""
Demonstrates some simple Timestamp operations
"""
from mw import Timestamp

# Seconds since Unix Epoch
str(Timestamp(1234567890))
# > '20090213233130'

# Database format
int(Timestamp("20090213233130"))
# > 1234567890

# API format
int(Timestamp("2009-02-13T23:31:30Z"))
# > 1234567890

# Difference in seconds
Timestamp("2009-02-13T23:31:31Z") - Timestamp(1234567890)
# > 1

# strptime and strftime
Timestamp(1234567890).strftime("%Y foobar")
# > '2009 foobar'

str(Timestamp.strptime("2009 derp 10", "%Y derp %m"))
# > '20091001000000'
