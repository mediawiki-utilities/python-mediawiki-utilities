from itertools import chain

from nose.tools import eq_
from .. import defaults
from ..functions import sessions


EVENTS = {
    "foo": [
        [
            ("foo", 1234567890, 1),
            ("foo", 1234567892, 2),
            ("foo", 1234567894, 3)
        ],
        [
            ("foo", 1234567894 + defaults.CUTOFF, 4),
            ("foo", 1234567897 + defaults.CUTOFF, 5)
        ]
    ],
    "bar": [
        [
            ("bar", 1234567891, 6),
            ("bar", 1234567892, 7),
            ("bar", 1234567893, 8)
        ],
        [
            ("bar", 1234567895 + defaults.CUTOFF, 9),
            ("bar", 1234567898 + defaults.CUTOFF, 0)
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
        eq_(list(e[2] for e in EVENTS[user][counts[user]]), list(session))
        counts[user] += 1
