import sys; sys.path.insert(0, "../")

from mwutil.dump import Iterator

# Construct dump file iterator
dump = Iterator.from_file(open("examples/dump.xml"))

# Iterate through pages
for page in dump:

		# Iterate through a page's revisions
		for revision in page:

				print(revision.id)
