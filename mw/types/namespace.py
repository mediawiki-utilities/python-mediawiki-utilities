from ..util import none_or

from . import serializable

class Namespace(serializable.Type):
	
	__slots__ = ('id', 'name', 'aliases', 'case', 'canonical')
	
	def __init__(self, id, name, canonical=None, aliases=None, case=None):
		self.id = int(id)
		self.name = none_or(name, str)
		self.aliases = serializable.Set.deserialize(aliases or [], str)
		self.case = none_or(case, str)
		self.canonical = none_or(canonical, str)
	
	def __hash__(self): return self.id
