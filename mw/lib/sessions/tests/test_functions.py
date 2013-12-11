from nose.tools import eq_
from itertools import chain 

from ..functions import group_events, DEFAULT_CUTOFF
from ..event import Event

USER_EVENTS = {
	"foo": [
		[
			Event("foo", 1234567890, None),
			Event("foo", 1234567892, None),
			Event("foo", 1234567894, None)
		],
		[
			Event("foo", 1234567894+DEFAULT_CUTOFF, None),
			Event("foo", 1234567897+DEFAULT_CUTOFF, None)
		]
	],
	"bar": [
		[
			Event("bar", 1234567891, None),
			Event("bar", 1234567892, None),
			Event("bar", 1234567893, None)
		],
		[
			Event("bar", 1234567895+DEFAULT_CUTOFF, None),
			Event("bar", 1234567898+DEFAULT_CUTOFF, None)
		]
	]
}

def test_group_events():
	events = []
	events.extend(chain(*USER_EVENTS['foo']))
	events.extend(chain(*USER_EVENTS['bar']))
	
	events.sort(key=lambda e:e.timestamp)
	
	user_sessions = group_events(events)
	
	counts = {
		'foo': 0,
		'bar': 0
	}
	
	for user, session in user_sessions:
		eq_(USER_EVENTS[user][counts[user]], list(session))
		counts[user] += 1
