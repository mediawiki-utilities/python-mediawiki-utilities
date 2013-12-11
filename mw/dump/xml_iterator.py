import xml.etree.ElementTree as etree

def XMLIterator(fp):
	xmlIterator = etree.iterparse(fp, events=("start","end"))
	event, element = next(xmlIterator)
	return ElementIterator(element, xmlIterator)
	
class ElementIteratorError: pass

class ElementIterator:
	
	def __init__(self, element, xmlIterator):
		self.element     = element
		self.xmlIterator = xmlIterator
		self.tagStack    = [self.element.tag]
		
	def __iter__(self):
		if len(self.tagStack) == 0:
			raise ElementIteratorError("Element has already been iterated through.")
		
		for event, element in self.xmlIterator:
			if event == "start":
				element = ElementIterator(element, self.xmlIterator)
				yield element
				element.clear()
			
			else: #event == "end"
				assert element.tag == self.element.tag, "Expected %r, got %r" % (self.element.tag, element.tag)
				self.tagStack.pop()
			
			if len(self.tagStack) == 0:
				break
			
			
	def get(self, key, alt=None):
		return self.element.attrib.get(key, alt)
		
	
	def complete(self):
		if len(self.tagStack) != 0:
			for event, element in self.xmlIterator:
				if event == "start":
					self.tagStack.append(element.tag)
					element.clear()
				
				else: #event == "end"
					#assert self.tagStack[-1] == element.tag, "Expected %r at the end of %r" % (element.tag, self.tagStack)
					self.tagStack.pop()
				
				if len(self.tagStack) == 0:
					break
			
		
	def clear(self):
		self.complete()
		self.element.clear()
	
	def __del__(self):
		self.clear()
	
	def __getattr__(self, attr):
		if attr == "attrib":
			return self.element.attrib
		elif attr == "tag":
			return self.element.tag
		elif attr == "tail":
			return self.element.tail
		elif attr == "text":
			self.complete()
			return self.element.text
		else:
			raise AttributeError("%s has no attribute %r" % (self.__class__.__name__, attr))
				
