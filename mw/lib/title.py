"""
A set of utilities for parsing and normalizing MediaWiki page names and titles. 

For use in this 
"""

@classmethod
def normalize(title):
	if title == None: 
		return title
	else:
		return title.capitalize().replace(" ", "_")

def Namespaces(*args, **kwargs):
	if isinstance(args[0], NamespacesType):
		return namespaces
	else:
		return NamespacesType(*args, **kwargs)

class NamespacesType:
	
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
		
	def __contains__(self, name):
		return self.contains(name=name)
	
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
		self.namespaces = Namespaces(namespaces)
		
	def parse(page_name):
		parts = page_name.split(":", 1)
		if len(parts) == 1:
			ns_id = 0
			title = normalize(page_name)
		else:
			ns_name, title = parts
			ns_name, title = normalize(ns_name), normalize(ns_title)
			
			if ns_name in self.namespaces:
				ns_id = self.namespaces.get(name=ns_name).id
			else:
				ns_id = 0
				title = normalize(page_name)
			
		
		return ns_id, title
