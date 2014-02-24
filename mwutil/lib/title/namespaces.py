from ...util import autovivifying
from .functions import normalize
from .namespace import Namespace

def Namespaces(*args, **kwargs):
	if isinstance(args[0], NamespacesType):
		return namespaces
	else:
		return NamespacesType(*args, **kwargs)

Namespaces.from_site_info = lambda si_doc: NamespacesType.from_site_info(si_doc)
	

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
		
		for alias in namespace.aliases:
			self.names[alias] = namespace
		
		if namespace.canonical != None: 
			self.names[namespace.canonical] = namespace
		
		
		
	def __contains__(self, name):
		return self.contains(name=name)
	
	def contains(self, id=None, name=None):
		if id != None:
			return int(id) in self.ids
		else:
			return normalize(name) in self.names
	
	def get(self, id=None, name=None):
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
			
			if ns_name in self:
				ns_id = self.get(name=ns_name).id
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
			
			names = [ns_doc['*']]
			if 'canonical' in ns_doc: names.insert(0, ns_doc['canonical'])
			
			namespaces.append(
				Namespace(
					ns_doc['id'], 
					names, 
					canonical=ns_doc.get('canonical'),
					aliases=aliases[ns_doc['id']],
					case=ns_doc['case']
				)
			)
		
		
		
		return NamespacesType(namespaces)
	
	@classmethod
	def from_dump(cls, namespaces):
		raise NotImplementedError
	
