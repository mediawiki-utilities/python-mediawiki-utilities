import oursql, sys
from mwlib.database import DB

db1047 = oursql.connect(
	host="db1047.eqiad.wmnet",
	user="halfak",
	database="enwiki"
	defaults_file="~/.my.cnf"
)

db = DB(db1047)

for line in sys.stdin:
	user_id = int(line)
	
	stats = db.users.newcomer_stats(user_id, lifetime=60*60*24*7)
	
	print("\t".join(user_id, stats.revisions, stats.reverted.))
