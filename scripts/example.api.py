"""
Prints the rev_id of all revisions to User:EpochFail.
"""
import sys;sys.path.append("../")
from mw import api

api = api.Session("https://en.wikipedia.org/w/api.php")

revisions = api.revisions.query(
	properties={'ids'},
	titles={'User:EpochFail'}
)

for rev in revisions:
	print(rev['revid'])
