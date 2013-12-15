"""
Prints the stats of a list of users (passed through stdin)
"""
import oursql, sys
from mwlib.database import DB
from mwlib.database.generators import NewcomerStats

db1047 = oursql.connect(
	host="db1047.eqiad.wmnet",
	user="halfak",
	database="enwiki"
	defaults_file="~/.my.cnf"
)

db = DB(db1047)

newcomer_stats = NewcomerStats(db)

for line in sys.stdin:
	user_id = int(line)
	
	# stats for first week
	stats = newcomer_stats.calculate(user_id, lifetime=60*60*24*7)
	
	print("\t".join(user_id, stats.revisions, stats.reverted))
