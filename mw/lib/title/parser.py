
from ...types import Namespace
from ...util import autovivifying

from .functions import normalize
	

class Parser:
	
	def __init__(self, namespaces=None):
		self.ids   = {}
		self.names = {}
		
		if namespaces != None:
			for namespace in namespaces:
				self.add(namespace)
	
	def add(self, namespace):
		self.ids[namespace.id] = namespace
		self.names[namespace.name] = namespace
		
		for alias in namespace.aliases:
			self.names[alias] = namespace
		
		if namespace.canonical != None: 
			self.names[namespace.canonical] = namespace
		
	
	def contains_name(self, name):
		return normalize(name) in self.names
	
	def get_namespace(self, id=None, name=None):
		if id != None:
			return self.ids[int(id)]
		else:
			return self.names[normalize(name)]
		
	def parse(self, page_name):
		parts = page_name.split(":", 1)
		if len(parts) == 1:
			ns_id = 0
			title = normalize(page_name)
		else:
			ns_name, title = parts
			ns_name, title = normalize(ns_name), normalize(title)
			
			if self.contains_name(ns_name):
				ns_id = self.get_namespace(name=ns_name).id
			else:
				ns_id = 0
				title = normalize(page_name)
			
		
		return ns_id, title
	
	@classmethod
	def from_site_info(cls, si_doc):
		
		aliases = autovivifying.Dict(vivifier=lambda k:[])
		# get aliases
		if 'namespacealiases' in si_doc:
			for alias_doc in si_doc['namespacealiases']:
				aliases[alias_doc['id']].append(alias_doc['*'])
			
		
		namespaces = []
		for ns_doc in si_doc['namespaces'].values():
			
			namespaces.append(
				Namespace(
					ns_doc['id'], 
					ns_doc['*'], 
					canonical=ns_doc.get('canonical'),
					aliases=aliases[ns_doc['id']],
					case=ns_doc['case']
				)
			)
		
		
		
		return Parser(namespaces)
	
	@classmethod
	def from_api(cls, session):
		
		si_doc = session.site_info.query(
			properties={'namespaces', 'namespacealiases'}
		)
		
		return cls.from_site_info(si_doc)
	
	@classmethod
	def from_dump(cls, namespaces):
		raise NotImplementedError
	
