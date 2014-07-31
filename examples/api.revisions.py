"""
Prints the rev_id, characters and hash of all revisions to User:EpochFail.
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.getcwd()))

import hashlib
from mw import api

api_session = api.Session("https://en.wikipedia.org/w/api.php")

revisions = api_session.revisions.query(
    properties={'ids', 'content'},
    titles={"User:EpochFail"},
    direction="newer",
    limit=51
)

for rev in revisions:
    print(
        "{0} ({1} chars): {2}".format(
            rev['revid'],
            len(rev.get('*', "")),
            hashlib.sha1(bytes(rev.get('*', ""), 'utf8')).hexdigest()
        )
    )
