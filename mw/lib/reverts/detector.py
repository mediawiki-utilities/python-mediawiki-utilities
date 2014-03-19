from collections import namedtuple

from ...util import ordered
from . import defaults

Revert = namedtuple("Revert", ['reverting', 'reverteds', 'reverted_to'])
"""
Represents a reverting revision (`reverting`), the revision that was reverted 
to (`reverted_to`) and the intervening revisions that were reverted 
(`reverteds`).
"""

class Detector(ordered.HistoricalMap):
	"""
	Detects reverts in a stream of revisions (to the same page) based on 
	matching checksums.  See https://meta.wikimedia.org/wiki/R:Identity_revert
	"""
	
	def __init__(self, radius=defaults.RADIUS):
		"""
		:Parameters:
			radius : int
				The maximum number of revisions that a revert can span.
		"""
		super().__init__(maxlen=radius+1)
		
	def process(self, checksum, revision=None):
		"""
		Processes a new revision and returns revert data if a revert occured.
		"""
		revert = None
		
		if checksum in self: #potential revert
			
			reverteds = list(self.up_to(checksum))
			
			if len(reverteds) > 0: # If no reverted revisions, this is a noop
				revert = Revert(revision, reverteds, self[checksum])
			
		self.insert(checksum, revision)
		return revert
