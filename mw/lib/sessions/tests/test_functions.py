from nose.tools import eq_
from itertools import chain 

from .. import defaults
from ..functions import sessions

EVENTS = {
	"foo": [
		[
			("foo", 1234567890, None),
			("foo", 1234567892, None),
			("foo", 1234567894, None)
		],
		[
			("foo", 1234567894+defaults.CUTOFF, None),
			("foo", 1234567897+defaults.CUTOFF, None)
		]
	],
	"bar": [
		[
			("bar", 1234567891, None),
			("bar", 1234567892, None),
			("bar", 1234567893, None)
		],
		[
			("bar", 1234567895+defaults.CUTOFF, None),
			("bar", 1234567898+defaults.CUTOFF, None)
		]
	]
}

def test_group_events():
	events = []
	events.extend(chain(*EVENTS['foo']))
	events.extend(chain(*EVENTS['bar']))
	
	events.sort()
	
	user_sessions = sessions(events)
	
	counts = {
		'foo': 0,
		'bar': 0
	}
	
	for user, session in user_sessions:
		eq_(EVENTS[user][counts[user]], list(session))
		counts[user] += 1
