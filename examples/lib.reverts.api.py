import sys,os;sys.path.insert(0, os.path.abspath(os.getcwd()))
from mw.api import Session
from mw.lib import reverts

session = Session("https://en.wikipedia.org/w/api.php")
revisions = session.user_contribs.query(user={"PermaNoob"})

for rev in revisions:
	revert = reverts.api.check_rev(session, rev)
	if revert != None: 
		print("{0} reverted {1} to {2}".format(
				revert.reverting['revid'],
				rev['revid'],
				revert.reverted_to['revid']
			)
		)

