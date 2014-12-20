"""
Prints the rev_id and hash of the 10 oldest recent changes
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
    properties={'ids', 'sha1', 'timestamp'},
    direction="newer",
    limit=10
)

for change in changes:
    print(
        "{0} ({1}): {2}".format(
            change['timestamp'],
            change['revid'],
            change.get('sha1', "")
        )
    )
