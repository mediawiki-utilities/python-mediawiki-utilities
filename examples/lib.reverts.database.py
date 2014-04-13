import sys,os;sys.path.insert(0, os.path.abspath(os.getcwd()))
from mw.database import DB
from mw.lib import reverts

db = DB(host="s1-analytics-slave.eqiad.wmnet", read_default_file="~/.my.cnf", user="research", db="enwiki")
revisions = db.revisions.query(user_id=9133062)

for rev_row in revisions:
	revert = reverts.database.check_row(db, rev_row)
	if revert != None: 
		print("{0} reverted {1} to {2}".format(
				revert.reverting['rev_id'],
				rev_row['rev_id'],
				revert.reverted_to['rev_id']
			)
		)

