RADIUS = 15
"""
TODO: Better documentation here.  For the time being, see:

Priedhorsky, R., Chen, J., Lam, S. T. K., Panciera, K., Terveen, L., &
Riedl, J. (2007, November). Creating, destroying, and restoring value in
Wikipedia. In Proceedings of the 2007 international ACM conference on
Supporting group work (pp. 259-268). ACM.
"""


class DUMMY_SHA1: pass
"""
Used in when checking for reverts when the checksum of the revision of interest
is unknown.

>>> DUMMY_SHA1 in {"aaa", "bbb"} # or any 40 character hex
False
>>>
>>> DUMMY_SHA1 == DUMMY_SHA1
True
>>> {DUMMY_SHA1, DUMMY_SHA1}
{<class '__main__.DUMMY_SHA1'>}
"""
