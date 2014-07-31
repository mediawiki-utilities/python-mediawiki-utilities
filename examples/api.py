"""
Prints the rev_id of all revisions to User:EpochFail.
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.getcwd()))

from mw import api

api_session = api.Session("https://en.wikipedia.org/w/api.php")

revisions = api_session.revisions.query(
    properties={'ids'},
    titles={'User:TestAccountForMWUtils'}
)

for rev in revisions:
    print(rev['revid'])
