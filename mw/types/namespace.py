from ..lib import title
from ..util import none_or

class Namespace:
	
	__slots__ = ('id', 'names', 'case', 'canonical')
	
	def __init__(self, id, names, canonical=None, case=None):
		self.id = int(id)
		self.names = set(title.normalize(n) for n in names)
		self.case = none_or(case, str)
		
		if canonical == None:
			self.canonical = title.normalize(names[0])
		else:
			canonical = title.normalize(canonical)
			
			if canonical not in self.names:
				raise KeyError(canonical)
			self.canonical = canonical
		
