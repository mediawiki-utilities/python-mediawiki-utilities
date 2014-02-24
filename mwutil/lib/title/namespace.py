from ...util import none_or

from .functions import normalize

class Namespace:
	
	__slots__ = ('id', 'names', 'aliases', 'case', 'canonical')
	
	def __init__(self, id, names, canonical=None, aliases=None, case=None):
		self.id = int(id)
		self.names = set(normalize(n) for n in names)
		self.aliases = set(normalize(a) for a in (aliases or []))
		self.case = none_or(case, str)
		
		self.canonical = none_or(canonical, normalize)
		
