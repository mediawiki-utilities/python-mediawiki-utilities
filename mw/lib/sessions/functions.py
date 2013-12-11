import logging

from .constants import DEFAULT_CUTOFF
from .event import Event
from .session_manager import SessionManager

logger = logging.getLogger("mw.lib.sessions.functions")

def sessions(user_timestamp_sessions, cutoff=DEFAULT_CUTOFF):
	return group_events((Event(*uts) for uts in user_timestamp_sessions), 
	                    cutoff=cutoff)


def group_events(events, cutoff=DEFAULT_CUTOFF):
	
	events = (Event(e) for e in events)
	
	session_manager = SessionManager(cutoff)
	
	for event in events:
		
		for user, session in session_manager.process(event):
			yield user, session
		
	
	for user, session in session_manager.get_active_sessions():
		yield user, session

"""
def _pre_grouped(user_events, cutoff=DEFAULT_CUTOFF):
	
	grouped_events = iteration.group(user_events, by=lambda e: e.user)
	
	for user, events in grouped_events:
		
		for session in _group_user_sessions(events, cutoff):
			yield user, session
			deque(session, maxlen=0) # Consumes any leftovers
		
	
def _group_user_sessions(events, cutoff=DEFAULT_CUTOFF):
	
	#events = list(events);print(events)
	events = iteration.Peekable(events)
	
	while not events.empty():
		yield list(_group_user_session(events, cutoff))

def _group_user_session(events, cutoff=DEFAULT_CUTOFF):
	last = None
	while not events.empty():
		if last == None: print(events.peek())
		if last == None or events.peek().timestamp - last.timestamp < cutoff:
			event = events.next()
			yield event
			last = event
		else:
			#print(events.peek().timestamp - last.timestamp)
			break
		
"""
