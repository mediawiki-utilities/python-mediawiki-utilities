import logging
from ...types import Timestamp

logger = logging.getLogger("mw.lib.sessions.event")

def Event(*args, **kwargs):
	if len(args) == 1 and isinstance(args[0], EventType):
		return args[0]
	else:
		return EventType(*args, **kwargs)

class EventType:
	
	__slots__ = ('user', 'timestamp', 'data')
			
	def __init__(self, user, timestamp, data=None):
		self.user = user
		self.timestamp = Timestamp(timestamp)
		self.data = data
		
	def __str__(self): return self.__repr__()
	
	def __repr__(self):
		return "{0}({1})".format(
			self.__class__.__name__,
			", ".join([repr(v) for v in [self.user, self.timestamp, self.data]])
		)
	
	def __eq__(self, other):
		try:
			return (
				self.user == other.user and
				self.timestamp == other.timestamp and
				self.data == other.data
			)
		except AttributeError:
			return False
		
	
