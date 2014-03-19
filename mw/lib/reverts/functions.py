
from .detector import Detector
from . import defaults

def detect(checksum_revisions, radius=defaults.RADIUS):
	"""
	Detects identity reverts that occur in a sequence of revisions based on 
	matching checksums and limited by a radius -- the maximum distance that a
	revert can span.
	
	:Parameters:
		checksum_revisions : iterable
			an iterable of checksums and revisions 
	
	:Return:
		a generator of (reverting, reverteds, reverted_to) for each reverting revision
	"""
	
	revert_detector = Detector(radius)
	
	for checksum, revision in checksum_revisions:
		revert = revert_detector.process(checksum, revision)
		if revert != None: yield revert
		
# For backwards compatibility
reverts = detect


