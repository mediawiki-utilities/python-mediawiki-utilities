from nose.tools import eq_
from itertools import chain 

from ..functions import DEFAULT_CUTOFF
from ..event import Event
from ..session_manager import SessionManager

def test_session_manager():
	manager = SessionManager(cutoff=2)
	
	user_sessions = list(manager.process(Event("foo", 1)))
	eq_(user_sessions, [])
	
	user_sessions = list(manager.process(Event("bar", 2)))
	eq_(user_sessions, [])
	
	user_sessions = list(manager.process(Event("foo", 2)))
	eq_(user_sessions, [])
	
	user_sessions = list(manager.process(Event("bar", 10)))
	eq_(len(user_sessions), 2)
	
	user_sessions = list(manager.get_active_sessions())
	eq_(len(user_sessions), 1)
	
	
	
