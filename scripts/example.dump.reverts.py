"""
Prints the data about reverted revisions (rev_id, reverting_id, timediff).
"""
import sys

from mw import dump
from mw.lib import reverts

dump = dump.Iterator(sys.stdin)

for page in dump:
	
	checksum_revisions = (rev.sha1, rev for rev in page)
	
	for reverting, reverteds, reverted_to in reverts.reverts(checksum_revisions):
		
		for reverted in reverteds:
			print "\t".join(
				str(v) for v in [reverted.id, reverting.id, 
				                 reverting.timestamp - reverted.timestamp]
			)



