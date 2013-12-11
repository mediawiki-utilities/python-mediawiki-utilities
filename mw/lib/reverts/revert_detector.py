
from ..util import ordered

class RevertDetector(ordered.HistoricalMap):
	
	def __init__(self, radius):
		super().__init__(self, radius)
		
	def _process(self, checksum, revision):
		revert = None
		
		if checksum in self: #potential revert
			
			reverteds = list(self.up_to(checksum))
			
			if len(reverts) > 0:
				revert = (revisions, reverteds, self[checksum])
			else:
				#noop!
			
		
		self.insert(checksum, revision)
		
		return revert
		
	
	def process(self, checksum_revisions):
		
		for checksum, revision in checksum_revision:
			
			revert = self._process(checksum, revision)
			if revert != None: yield revert
