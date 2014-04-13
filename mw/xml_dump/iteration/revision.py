from ...types import serializable, Timestamp
from ...util import none_or

from .contributor import Contributor
from .util import consume_tags

class Revision(serializable.Type):
	"""
	Revision meta data.
	"""
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
	
	def __init__(self, id, timestamp, contributor=None, minor=None, 
	             comment=None, text=None, bytes=None, sha1=None, 
	             parent_id=None, model=None, format=None):
		self.id          = int(id)
		"""
		Revision ID : int
		"""
		
		self.timestamp   = Timestamp(timestamp)
		"""
		Revision timestamp : :class:`mw.Timestamp`
		"""
		
		self.contributor = none_or(contributor, Contributor.deserialize)
		"""
		Contributor meta data : :class:`~mw.xml_dump.Contributor` | `None`
		"""
		
		self.minor       = False or none_or(minor, bool)
		"""
		Is revision a minor change? : bool
		"""
		
		self.comment     = none_or(comment, str)
		"""
		Comment left with revision : str
		"""
		
		self.text        = none_or(text, str)
		"""
		Content of revision : str
		"""
		
		self.bytes       = none_or(bytes, int)
		"""
		Number of bytes of content
		"""
		
		self.sha1        = none_or(sha1, str)
		"""
		sha1 hash of the content
		"""
		
		self.parent_id   = none_or(parent_id, int)
		"""
		Revision ID of preceding revision : int | `None`
		"""
		
		self.model       = none_or(model, str)
		"""
		TODO: ??? : str
		"""
		
		self.format      = none_or(format, str)
		"""
		TODO: ??? : str
		"""
	
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
		


