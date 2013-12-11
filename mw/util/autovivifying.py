	
class Dict(dict):
	
	def __init__(self, *args, **kwargs):
		if 'vivifier' in kwargs:
			self.vivifier = kwargs['vivifier']
		else:
			raise TypeError("Argument vivifier must be provided")
		
		del kwargs['vivifier']
		
		dict.__init__(self, *args, **kwargs)
	
	def __getitem__(self, key):
		if key not in self:
			dict.__setitem__(self, key, self.vivifier(key))
				
		return dict.__getitem__(self, key)
