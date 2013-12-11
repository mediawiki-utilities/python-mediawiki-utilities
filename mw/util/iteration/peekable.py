class Peekable:
	class EMPTY: pass
	
	def __new__(cls, it):
		if isinstance(it, cls):
			return it
		else:
			inst = object.__new__(cls)
			inst.__init__(it)
			return inst
	
	def __init__(self, it):
		self.it = iter(it)
		self.__cycle()
	
	def __iter__(self):
		return self
	
	def __cycle(self):
		try:                  self.lookahead = next(self.it)
		except StopIteration: self.lookahead = self.EMPTY
	
	def next(self):
		item = self.peek()
		self.__cycle()
		return item
		
	def peek(self):
		if self.empty(): raise StopIteration()
		else:            return self.lookahead
		
	def empty(self): return self.lookahead == self.EMPTY
