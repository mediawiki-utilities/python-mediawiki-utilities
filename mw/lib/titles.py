"""
A set of utilities for parsing and normalizing MediaWiki page names and titles. 
"""

@classmethod
def normalize_title(title):
	if title == None: 
		return title
	else:
		return title.capitalize().replace(" ", "_")

@classmethod
def parse_page_name(page_name, namespaces):
	page_name = cls.normalize(page_name)
	
	parts = page_name.split(":", 1)
	if len(parts) == 1:
		ns_id = 0
		title = page_name
	else:
		ns_name, title = parts
		
		if namespace.contains(name=ns_nane):
			ns_id = namespaces.get(name=ns_name).id
			title = cls.normalize(title)
		else:
			ns_id = 0
			title = page_name
		
	
	return ns_id, title
	


	
	

class Namespaces:
	
	def __init__(self, namespaces=None):
		self.ids   = {}
		self.names = {}
		
		if namespaces != None:
			for namespace in namespaces:
				self.add(namespace)
	
	def add(self, namespace):
		self.ids[namespace.id] = namespace
		for name in namespace.names:
			self.names[name] = namespace
		
	def contains(self, id=None, name=None):
		if id != None:
			return int(id) in self.ids
		else:
			return normalize_title(name) in self.names
	
	def get(self, id=None, name=None):
		if id != None:
			return self.ids[int(id)]
		else:
			return self.names[normalize_title(name)]
	
	@classmethod
	def from_site_info(cls, si_doc):
		
		namespaces = (
			Namespace(ns_doc['id'], [ns_doc['canonical'], ns_doc['*']], 
				      canonical=ns_doc['canonical'], case=ns_doc['case'])
			for ns_doc in si_doc['query']['namespaces'].values()
		)
		
		return namespaces
	
	@classmethod
	def from_dump(cls, namespaces):
		
		namespaces = (
			Namespace(namespace.id, [namespace.name], canonical=namespace.name,
			          case=namespace.case)
			for id, namespace in si_doc['query']['namespaces'].values()
		)
		
		return namespaces
	
	
class Parser:
	
	def __init__(self, namespaces):
		
