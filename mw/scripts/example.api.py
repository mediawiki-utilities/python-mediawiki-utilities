"""
Prints the rev_id of all revisions to User:EpochFail.
"""
from mwlib.api import API

en_api = API("https://en.wikipedia.org/w/api.php")

revisions = en_api.revisions.query(
	properties=['ids','flags','comment','tags'],
	titles=['User:EpochFail']
)


for rev in revisions:
	print(rev['revid'])
