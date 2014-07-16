import sys,os;sys.path.insert(0, os.path.abspath(os.getcwd()))

from mw.xml_dump import Iterator

# Construct dump file iterator
dump = Iterator.from_file(open("examples/dump.xml"))

# Iterate through pages
for page in dump:

        # Iterate through a page's revisions
        for revision in page:

                print(revision.id)
