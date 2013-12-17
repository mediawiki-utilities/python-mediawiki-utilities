
from ...util import ordered
from . import defaults

class Detector(ordered.HistoricalMap):
	
	def __init__(self, radius=defaults.RADIUS):
		super().__init__(maxlen=radius+1)
		
	def process(self, checksum, revision=None):
		revert = None
		
		if checksum in self: #potential revert
			
			reverteds = list(self.up_to(checksum))
			
			if len(reverteds) > 0: # If no reverted revisions, this is a noop
				return (revision, reverteds, self[checksum])
			
		self.insert(checksum, revision)
