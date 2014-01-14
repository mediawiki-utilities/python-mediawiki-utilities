
class Type(object):
	
	
	def __eq__(self, other):
		try:
			for key in self.__dict__:
				if self.__dict__[key] == other.__dict__[key]: pass
				else: return False
			
			return True
		except KeyError:
			return False
	
	def __neq__(self, other):
		return not self.__eq__(other)
	
	def __str__(self): return self.__repr__()
	
	def __repr__(self):
		return "%s(%s)" % (
			self.__class__.__name__,
			", ".join(
				"%s=%r" % (k, v) for k, v in self.__dict__.iteritems()
			)
		)
		
	def serialize(self):
		return dict(
			(k, self._serialize(v)) 
			for k, v in self.__dict__.iteritems()
		)
	
	def _serialize(self, value):
		if hasattr(value, "serialize"):
			return value.serialize()
		else:
			return value
	
	@classmethod
	def deserialize(cls, doc_or_instance):
		if isinstance(doc_or_instance, cls):
			return doc_or_instance
		else:
			return cls(**doc_or_instance)
	

class Dict(dict, Type):
	
	def serialize(self):
		return {k: self._serialize(v) for k, v in self.iteritems()}
	
	@staticmethod
	def deserialize(cls, d):
		
		if isinstance(d, Dict):
			return d
		else:
			return Dict((k, cls.deserialize(v)) for k, v in d.iteritems())


class List(list, Type):
	
	def serialize(self):
		return list(self._serialize(v) for v in self)
	
	@staticmethod
	def deserialize(cls, l):
		
		if isinstance(l, List):
			return l
		else:
			return List(cls.deserialize(v) for v in l)
