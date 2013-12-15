"""
Prints the revision ids of all talk pages contained in a dump file.
"""
import sys
from mw.dump import Dump

xml_dump = Dump(sys.stdin)

ns_map = {}
for namespace in xml_dump.info.namespaces:
	ns_map[namespace.key] = namespace.name

for page in xml_dump:
	
	# If the page is a talk page
	if page.namespace % 2 == 1:
		
		# Read all the revisions
		for revision in page:
			
			# Print out the revisions ids
			print(revision.id)
