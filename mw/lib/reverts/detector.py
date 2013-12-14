
from ...util import ordered

class Detector(ordered.HistoricalMap):
	
	def __init__(self, radius):
		super().__init__(maxlen=radius+1)
		
	def _process(self, checksum, revision):
		revert = None
		
		if checksum in self: #potential revert
			
			reverteds = list(self.up_to(checksum))
			
			if len(reverteds) > 0:
				revert = (revision, reverteds, self[checksum])
			else:
				pass #noop!
			
		
		self.insert(checksum, revision)
		
		return revert
		
	
	def process(self, checksum_revisions):
		
		for checksum, revision in checksum_revisions:
			
			revert = self._process(checksum, revision)
			if revert != None: yield revert
