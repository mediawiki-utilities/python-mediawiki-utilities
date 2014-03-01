from ...types import serializable, Timestamp
from ...util import none_or

from .contributor import Contributor
from .util import consume_tags

class Revision(serializable.Type):
	__slots__ = ('id', 'timestamp', 'contributor', 'minor', 'comment', 'text',
	             'bytes', 'sha1', 'parent_id', 'model', 'format')
	
	TAG_MAP = {
		'id':          lambda e: int(e.text),
		'timestamp':   lambda e: Timestamp(e.text),
		'contributor': lambda e: Contributor.from_element(e),
		'minor':       lambda e: True,
		'comment':     lambda e: str(e.text),
		'text':        lambda e: str(e.text) if e.attr("deleted", None) == None else None,
		'sha1':        lambda e: str(e.text),
		'parentid':    lambda e: int(e.text),
		'model':       lambda e: str(e.text),
		'format':      lambda e: str(e.text)
	}
	
	def __init__(self, id, timestamp, contributor, minor, comment, text, bytes,
	                   sha1, parent_id, model, format):
	
		self.id          = int(id)
		self.timestamp   = Timestamp(timestamp)
		self.contributor = none_or(contributor, Contributor.deserialize)
		self.minor       = False or minor
		self.comment     = none_or(comment, str)
		self.text        = none_or(text, str)
		self.bytes       = none_or(bytes, int)
		self.sha1        = none_or(sha1, str)
		self.parent_id   = none_or(parent_id, int)
		self.model       = none_or(model, str)
		self.format      = none_or(format, str)
	
	@classmethod
	def from_element(cls, element):
		values = consume_tags(cls.TAG_MAP, element)
		
		return cls(
			values.get('id'),
			values.get('timestamp'),
			values.get('contributor'),
			values.get('minor') == True,
			values.get('comment'),
			values.get('text'),
			values.get('bytes'),
			values.get('sha1'),
			values.get('parentid'),
			values.get('model'),
			values.get('format')
		)
		


