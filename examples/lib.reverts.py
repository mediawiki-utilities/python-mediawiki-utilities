"""
Prints all reverted revisions of User:EpochFail.
"""
from mw.api import Session
from mw.lib import reverts

# Gather a page's revisions from the API
api_session = Session("https://en.wikipedia.org/w/api.php")
revs = api_session.revisions.query(
    titles={"User:EpochFail"},
    properties={'ids', 'sha1'},
    direction="newer"
)

# Creates a revsion event iterator
rev_events = ((rev['sha1'], rev) for rev in revs)

# Detect and print reverts
for revert in reverts.detect(rev_events):
    print("{0} reverted back to {1}".format(revert.reverting['revid'],
                                            revert.reverted_to['revid']))
