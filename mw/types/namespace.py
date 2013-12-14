from ..lib import titles

class Namespace:
	
	__slots__ = ('id', 'names', 'case', 'canonical')
	
	def __init__(self, names, id, canonical=None, case=None):
		self.id = int(id)
		self.names = set(titles.normalize(n) for n in names)
		self.case = none_or(case, str)
		
		if canonical == None:
			self.canonical = titles.normalize(names[0])
		else:
			assert canonical in self.names:
			self.canonical = titles.normalize(canonical)
		
