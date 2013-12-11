import logging

from ...util import Heap
from .constants import DEFAULT_CUTOFF

logger = logging.getLogger("mw.lib.sessions.session_manager")

class SessionManager:
	
	def __init__(self, cutoff=DEFAULT_CUTOFF):
		self.cutoff = int(cutoff)
		
		self.recently_active = Heap()
		self.active_users  = {}
	
	def process(self, event):
		
		for user, session in self._clear_expired(event.timestamp):
			yield user, session
		
		#Apply revision
		if event.user in self.active_users:
			session = self.active_users[event.user]
		else:
			session = []
			self.active_users[event.user] = session
			self.recently_active.push((event.timestamp, session))
			
		session.append(event)
	
	def get_active_sessions(self):
		for user, session in self.active_users.items():
			yield user, session
	
	def _clear_expired(self, timestamp):
		
		# Cull old sessions
		while (len(self.recently_active) > 0 and 
		       timestamp - self.recently_active.peek()[0] >= self.cutoff):
			
			_, session = self.recently_active.pop()
			
			if timestamp - session[-1].timestamp >= self.cutoff:
				del self.active_users[session[-1].user]
				yield session[-1].user, session
			else:
				self.recently_active.push((session[-1].timestamp, session))
