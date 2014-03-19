import logging

from . import defaults
from .event import Event
from .cache import Cache

from . import defaults

logger = logging.getLogger("mw.lib.sessions.functions")

def cluster(events, cutoff=defaults.CUTOFF):
	
	# Construct the session manager 
	cache = Cache(cutoff)
	
	# Apply the events
	for user, timestamp, data in events:
		
		for user, session in cache.process(user, timestamp, data):
			yield user, session
		
	# Yield the left-overs
	for user, session in cache.get_active_sessions():
		yield user, session
	

# For backwards compatibility
sessions = cluster
