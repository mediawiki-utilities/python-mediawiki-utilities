from nose.tools import eq_

from ..protection import Protection
from ..timestamp import Timestamp

TEST_PARAMS = (
	"[edit=autoconfirmed] (expires 23:31, 13 February 2009 (UTC)) " + 
	"[move=autoconfirmed] (expires 23:31, 13 February 2009 (UTC))\n"
)

def test_protection():
	eq_(
		[
			Protection("edit", "autoconfirmed", Timestamp("2009-02-13T23:31:00Z")),
			Protection("move", "autoconfirmed", Timestamp("2009-02-13T23:31:00Z")),
		],
		list(Protection.from_params(TEST_PARAMS))
	)
