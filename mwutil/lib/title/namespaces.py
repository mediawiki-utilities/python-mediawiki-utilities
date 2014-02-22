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
	
	@classmethod
	def from_site_info(cls, si_doc):
		
		aliases = autovivifying.Dict(vivifier=lambda k:[])
		# get aliases
		if 'namespacealiases' in si_doc['query']:
			for alias_doc in si_doc['query']['namespacealiases']:
				aliases[alias_doc['id']].append(alias_doc['*'])
			
		
		namespaces = []
		for ns_doc in si_doc['query']['namespaces'].values():
			
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
	
