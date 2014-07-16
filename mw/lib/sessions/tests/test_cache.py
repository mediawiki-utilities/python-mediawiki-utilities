from nose.tools import eq_

from ..cache import Cache


def test_session_manager():
    cache = Cache(cutoff=2)

    user_sessions = list(cache.process("foo", 1))
    eq_(user_sessions, [])

    user_sessions = list(cache.process("bar", 2))
    eq_(user_sessions, [])

    user_sessions = list(cache.process("foo", 2))
    eq_(user_sessions, [])

    user_sessions = list(cache.process("bar", 10))
    eq_(len(user_sessions), 2)

    user_sessions = list(cache.get_active_sessions())
    eq_(len(user_sessions), 1)
