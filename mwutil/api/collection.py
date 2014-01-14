import re

class Collection:
	
	
	TIMESTAMP = re.compile(r"[0-9]{4}-?[0-9]{2}-?[0-9]{2}T?" + 
	                       r"[0-9]{2}:?[0-9]{2}:?[0-9]{2}Z?")
	
	DIRECTIONS = {'newer', 'older'}
	
	def __init__(self, session):
		self.session = session
	
	def _check_direction(self, direction):
		if direction == None:
			return direction
		else:
			direction = str(direction)
			
			assert direction in {None} | self.DIRECTIONS, \
				"Direction must be one of {0}".format(self.DIRECTIONS)
			
			return direction
	
	def _check_timestamp(self, timestamp):
		if timestamp == None:
			return timestamp
		else:
			timestamp = str(timestamp)
			
			if not self.TIMESTAMP.match(timestamp):
				raise TypeError(
					"{0} is not formatted like ".format(repr(timestamp)) + 
					"a MediaWiki timestamp."
				)
				
			return timestamp
	
	def _items(self, items, none=True, levels=None, type=lambda val:val):
		
		if none and items == None:
			return None
		else:
			items = {str(type(item)) for item in items}
			
			if levels != None:
				levels = {str(level) for level in levels}
				
				assert len(items - levels) == 0, \
					"items {0} not in levels {1}".format(
						levels - items, levels)
				
			
			return "|".join(items)
