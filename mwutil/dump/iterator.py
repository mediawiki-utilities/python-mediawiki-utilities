from .element_iterator import ElementIterator

from ..types import Timestamp
from ..util import none_or

from .errors import MalformedXML

def consume_tags(tag_map, element):
	value_map = {}
	for sub_element in element:
		tag_name = sub_element.tag
		
		if tag_name in tag_map:
			value_map[tag_name] = tag_map[tag_name](sub_element)
	
	return value_map

class Iterator:
	"""
	XML Wiki Dump
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
	def load_namespaces(cls, element):
		namespaces = {}
		for sub_element in element:
			tag = sub_element.tag
			
			if tag == "namespace":
				namespace = Namespace.from_element(sub_element)
				namespaces[namespace.id] = namespace
			else:
				assert False, "This should never happen"
			
		return namespaces
	
	@classmethod
	def load_site_info(cls, element):
		
		site_name  = None
		base       = None
		generator  = None
		case       = None
		namespaces = {}
		
		for sub_element in element:
			if sub_element.tag == 'sitename':
				site_name = sub_element.text
			elif sub_element.tag == 'base':
				base = sub_element.text
			elif sub_element.tag == 'generator':
				generator = sub_element.text
			elif sub_element.tag == 'case':
				case = sub_element.text
			elif sub_element.tag == 'namespaces':
				namespaces = cls.load_namespaces(sub_element)
			
		
		return site_name, base, generator, case, namespaces
		
	@classmethod
	def load_pages(cls, element):
		
		for sub_element in element:
			tag = sub_element.tag
			
			if tag == "page":
				yield Page.from_element(sub_element)
			else:
				assert MalformedXML("Expected to see 'page'.  " + \
					               "Instead saw '{0}'".format(tag))
	
	@classmethod
	def from_element(cls, element):
		
		site_name  = None
		base       = None
		generator  = None
		case       = None
		namespaces = None
		
		# Consume <siteinfo>
		for sub_element in element:
			tag = sub_element.tag
			if tag == "siteinfo":
				site_name, base, generator, case, namespaces = cls.load_site_info(sub_element)
				break
			
		# Consume all <page>
		pages = cls.load_pages(element)
		
		return cls(site_name, base, generator, case, namespaces, pages)
	
	@classmethod 
	def from_file(cls, f):
		element = ElementIterator.from_file(f)
		assert element.tag == "mediawiki"
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
	def from_element(cls, element):
		return cls(
			element.attr('key'),
			element.attr('case'),
			element.text
		)
	


class Page:
	__slots__ = (
		'id',
		'title',
		'namespace',
		'redirect',
		'restrictions',
		'revisions'
	)
	
	def __init__(self, id, title, namespace, redirect, restrictions, revisions):
		self.id = none_or(id, int)
		self.title = none_or(title, str)
		self.namespace = none_or(namespace, int)
		self.redirect = none_or(redirect, str)
		self.restrictions = none_or(restrictions, str)
		
		# Should be a lazy generator
		self.revisions = revisions
		
	
	def __iter__(self):
		return self.revisions
		
	def __next__(self):
		return next(self.revisions)
	
	@classmethod
	def load_revisions(cls, first_revision, element):
		yield Revision.from_element(first_revision)
		
		for sub_element in element:
			tag = sub_element.tag
			
			if tag == "revision":
				yield Revision.from_element(sub_element)
			else:
				raise MalformedXML("Expected to see 'revision'.  " + \
					               "Instead saw '{0}'".format(tag))
			
	
	@classmethod
	def from_element(cls, element):
		title        = None
		namespace    = None
		id           = None
		redirect     = None
		restrictions = None
		
		first_revision = None
		
		# Consume each of the elements until we see <id> which should come last.
		for sub_element in element:
			tag = sub_element.tag
			if tag == "title":
				title = sub_element.text
			elif tag == "ns":
				namespace = sub_element.text
			elif tag == "id":
				id    = int(sub_element.text)
			elif tag == "redirect":
				redirect = sub_element.attr("title", None)
			elif tag == "restrictions":
				restrictions = sub_element.text
			elif tag == "revision":
				first_revision = sub_element
				break
				# Assuming that the first revision seen marks the end of page 
				# metadata.  I'm not too keen on this assumption, so I'm leaving
				# this long comment to warn whoever ends up maintaining this. 
			else:
				raise MalformedXML("Unexpected tag found when processing " + \
					               "a <page>: '{0}'".format(tag))
		
		# Assuming that I got here by seeing a <revision> tag.  See verbose
		# comment above. 
		revisions = cls.load_revisions(first_revision, element)
		
		
		return cls(id, title, namespace, redirect, restrictions, revisions)

class Revision:
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
		

class Contributor:
	__slots__ = ('id', 'user_text')
	
	TAG_MAP = {
		'id':       lambda e: int(e.text),
		'username': lambda e: str(e.text),
		'ip':       lambda e: str(e.text)
	}
	
	def __init__(self, id, user_text):
		self.id = none_or(id, int)
		self.user_text = none_or(user_text, str)
	
	@classmethod
	def from_element(cls, element):
		values = consume_tags(cls.TAG_MAP, element)
		
		return cls(
			values.get('id'),
			values.get('username', values.get('ip'))
		)
	

