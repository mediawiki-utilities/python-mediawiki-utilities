"""
Prints the rev_id, characters and hash of all revisions to User:EpochFail.
"""
import os
import sys

try:
    sys.path.insert(0, os.path.abspath(os.getcwd()))
    from mw import api
except:
    raise

api_session = api.Session("https://en.wikipedia.org/w/api.php")

changes = api_session.recent_changes.query(
    properties={'ids', 'sha1'},
    direction="newer",
    limit=100
)

for change in changes:
    print(
        "{0} ({1} chars): {2}".format(
            change['revid'],
            len(change.get('*', "")),
            change.get('sha1', "")
        )
    )
