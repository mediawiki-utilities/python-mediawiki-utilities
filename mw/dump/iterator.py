from .xml_iterator import XMLIterator

from ..types import Timestamp
from ..util import none_or

from .errors import MalformedXML

def clean_tag(ns, raw):
	if ns != None:
		return raw[len(ns):]
	else:
		return raw

def consume_tags(tag_map, element, ns=None):
	value_map = {}
	for sub_element in element:
		tag_name = clean_tag(ns, sub_element.tag)
		
		if tag_name in tag_map:
			value_map[tag_name] = tag_map[tag_name](sub_element, ns)
	
	return value_map

class Iterator:
	"""
	WikiFile dump processor.  This class constructs with a filepointer to a 
	Wikipedia XML dump file.
	"""
	__slots__ = ('site_name', 'base', 'generator', 'case', 'namespaces', 
	             'pages')
	
	def __init__(self, site_name, base, generator, case, namespaces, pages):
		
		self.site_name  = none_or(site_name, str)
		self.base       = none_or(base, str)
		self.generator  = none_or(generator, str)
		self.case       = none_or(case, str)
		self.namespaces = none_or(namespaces, dict)
		
		# Should be a lazy generator of page info
		self.pages = pages
	
	def __iter__(self):
		return self.pages
		
	def __next__(self):
		return next(self.pages)
	
	@classmethod
	def load_namespaces(cls, element, ns=None):
		namespaces = {}
		for sub_element in element:
			tag = clean_tag(ns, sub_element.tag)
			
			if tag == "namespace":
				namespace = Namespace.from_element(sub_element, ns)
				namespaces[namespace.id] = namespace
			else:
				assert False, "This should never happen"
			
		return namespaces
	
	@classmethod
	def load_site_info(cls, element, ns=None):
		
		site_name  = None
		base       = None
		generator  = None
		case       = None
		namespaces = {}
		
		for sub_element in element:
			tag = clean_tag(ns, sub_element.tag)
			
			if tag == 'sitename':
				site_name = sub_element.text
			elif tag == 'base':
				base = sub_element.text
			elif tag == 'generator':
				generator = sub_element.text
			elif tag == 'case':
				case = sub_element.text
			elif tag == 'namespaces':
				namespaces = cls.load_namespaces(sub_element, ns)
			
		
		return site_name, base, generator, case, namespaces
		
	@classmethod
	def load_pages(cls, element, ns=None):
		
		for sub_element in element:
			tag = clean_tag(ns, sub_element.tag)
			
			if tag == "page":
				yield Page.from_element(sub_element, ns)
			else:
				assert False, "This should never happen"
	
	@classmethod
	def from_element(cls, element):
		
		ns = element.tag[:-len('mediawiki')]
		
		site_name = None
		base      = None
		generator = None
		case      = None
		namespace = None
		
		# Consume <siteinfo>
		for sub_element in element:
			tag = clean_tag(ns, sub_element.tag)
			if tag == "siteinfo":
				site_name, base, generator, case, namespaces = cls.load_site_info(sub_element, ns)
				break
			
		# Consume all <page>
		pages = cls.load_pages(element, ns)
		
		return cls(site_name, base, generator, case, namespaces, pages)
	
	@classmethod 
	def from_file(cls, f):
		element = XMLIterator(f)
		return cls.from_element(element)
	

class Namespace:
	__slots__ = ('id', 'case', 'name')
	
	
	def __init__(self, id, case, name):
		self.id = int(id)
		self.case = str(case)
		self.name = str(name)
	
	def __repr__(self):
		return "{0}({1})".format(
			self.__class__.__name__,
			", ".join(
				repr(v) for v in [
					self.id,
					self.case,
					self.name
				]
			)
		)
		
	@classmethod
	def from_element(cls, element, ns=None):
		return cls(
			element.get('key'),
			element.get('case'),
			element.text
		)
	


class Page:
	__slots__ = ('id', 'title', 'namespace', 'revisions')
	
	def __init__(self, id, title, namespace, revisions):
		self.id = none_or(id, int)
		self.title = none_or(title, str)
		self.namespace = none_or(namespace, int)
		
		# Should be a lazy generator
		self.revisions = revisions
		
	
	def __iter__(self):
		return self.revisions
		
	def __next__(self):
		return next(self.revisions)
	
	@classmethod
	def load_revisions(cls, element, ns=None):
		for sub_element in element:
			tag = clean_tag(ns, sub_element.tag)
			
			if tag == "revision":
				yield Revision.from_element(sub_element, ns)
			else:
				raise MalformedXML("Expected to see 'revision'.  " + \
					               "Instead saw '{0}'".format(tag))
			
	
	@classmethod
	def from_element(cls, element, ns=None):
		title     = None
		namespace = None
		id        = None
		
		# Consume each of the elements until we see <id> which should come last.
		for sub_element in element:
			tag = clean_tag(ns, sub_element.tag)
			if tag == "title":
				title = sub_element.text
			elif tag == "ns":
				namespace = sub_element.text
			elif tag == "id":
				id    = int(sub_element.text)
				break # This should be the last element before revisions start.
				      # I don't feel great about this practice, so I thought
				      # I'd write a long enough note that future me (you) will
				      # take notice of what's going on here.
		
		# <revision>s should be the only left at this point
		revisions = cls.load_revisions(element, ns)
		
		return cls(id, title, namespace, revisions)

class Revision:
	__slots__ = ('id', 'timestamp', 'contributor', 'minor', 'comment', 'text',
	             'bytes', 'sha1', 'parent_id', 'model', 'format')
	
	TAG_MAP = {
		'id':          lambda e, ns: int(e.text),
		'timestamp':   lambda e, ns: Timestamp(e.text),
		'contributor': lambda e, ns: Contributor.from_element(e, ns),
		'minor':       lambda e, ns: True,
		'comment':     lambda e, ns: str(e.text),
		'text':        lambda e, ns: str(e.text) if e.get("deleted", None) == None else None,
		'sha1':        lambda e, ns: str(e.text),
		'parentid':    lambda e, ns: int(e.text),
		'model':       lambda e, ns: str(e.text),
		'format':      lambda e, ns: str(e.text)
	}
	
	def __init__(self, id, timestamp, contributor, minor, comment, text, bytes,
	                   sha1, parent_id, model, format):
	
		self.id          = int(id)
		self.timestamp   = Timestamp(timestamp)
		self.contributor = contributor # Might be None.
		self.minor       = False or minor
		self.comment     = none_or(comment, str)
		self.text        = none_or(text, str)
		self.bytes       = none_or(bytes, int)
		self.sha1        = none_or(sha1, str)
		self.parent_id   = none_or(parent_id, int)
		self.model       = none_or(model, str)
		self.format      = none_or(format, str)
	
	@classmethod
	def from_element(cls, element, ns=None):
		values = consume_tags(cls.TAG_MAP, element, ns)
		
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
		

class Contributor:
	__slots__ = ('id', 'user_text')
	
	TAG_MAP = {
		'id':       lambda e, ns: int(e.text),
		'username': lambda e, ns: str(e.text),
		'ip':       lambda e, ns: str(e.text)
	}
	
	def __init__(self, id, user_text):
		self.id = none_or(id, int)
		self.user_text = none_or(user_text, str)
	
	@classmethod
	def from_element(cls, element, ns=None):
		values = consume_tags(cls.TAG_MAP, element, ns)
		
		return cls(
			values.get('id'),
			values.get('username', values.get('ip'))
		)
	

