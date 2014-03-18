from ...types import serializable
from ...util import none_or

from .. import errors
from ..element_iterator import ElementIterator
from .namespace import Namespace
from .page import Page
from .util import consume_tags

class Iterator(serializable.Type):
	__slots__ = ('site_name', 'base', 'generator', 'case', 'namespaces', '__pages')
	
	def __init__(self, site_name, base, generator, case, namespaces, pages=None):
		
		self.site_name  = none_or(site_name, str)
		self.base       = none_or(base, str)
		self.generator  = none_or(generator, str)
		self.case       = none_or(case, str)
		self.namespaces = none_or(namespaces, dict)
		
		# Should be a lazy generator of page info
		self.__pages = pages
	
	def __iter__(self):
		return self.__pages
		
	def __next__(self):
		return next(self.__pages)
	
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

