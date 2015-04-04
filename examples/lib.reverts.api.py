"""
Prints the reverting rev_id, rev_id and reverted to rev_id of all reverted
revisions made by user "PermaNoob".
"""
from mw.api import Session
from mw.lib import reverts

session = Session("https://en.wikipedia.org/w/api.php")
revisions = session.user_contribs.query(user={"PermaNoob"}, direction="newer")

for rev in revisions:
    revert = reverts.api.check_rev(session, rev, window=60*60*24*2)
    if revert is not None:
        print("{0} reverted {1} to {2}".format(
            revert.reverting['revid'],
            rev['revid'],
            revert.reverted_to['revid'])
        )
