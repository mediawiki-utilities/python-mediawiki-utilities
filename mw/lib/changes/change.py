from ...types import Timestamp

CHANGE_TYPES = {}

def register(change_class):
	for rc_match in change_class.matches:
		CHANGE_TYPES[rc_match] = change_class
	
def from_api(rc_doc):
	match = Match.from_api(doc)
	
	if match in CHANGE_TYPES:
		return CHANGE_TYPES[match].from_api(doc)
	else:
		return None
	
def from_db(rc_row):
	match = Match.from_db(rc_row)
	
	if match in CHANGE_TYPES:
		return CHANGE_TYPES[match].from_db(rc_row)
	else:
		return None

class Change:
	
	event_matches = {}
	
	def __init__(self, rc_id, timestamp, comment, source=None):
		self.rc_id     = int(rc_id)
		self.timestamp = Timestamp(timestamp)
		self.comment   = str(comment)
	

class LogEvent:
	
	def __init__(self, log_id, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.log_id = int(log_id)
		


class Match:
	
	def __init__(self, type, action, has_rev_id):
		self.type       = str(type)
		self.action     = str(action)
		self.has_rev_id = str(has_rev_id)
	
	def __eq__(self, other):
		try:
			return (
				self.type == other.type and
				self.action == other.action and
				self.has_rev_id == other.has_rev_id
			)
		except AttributeError:
			return False
	
	def __hash__(self):
		return hash(self.type, self.action, self.has_rev_id)
	
	@classmethod
	def from_api(self, rc_doc):
		return cls(doc['logtype'], doc['logaction'], doc['revid'] > 0)
	
	@classmethod
	def from_db(self, rc_row):
		return cls(doc['rc_log_type'], doc['rc_log_action'], doc['rc_this_oldid'] > 0)

