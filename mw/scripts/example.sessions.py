from mw.lib import sessions
from mw.api import API
from mw.types import Timestamp

api = API("http://en.wikipedia.org/w/api.php")

revs = api.revisions.query(user="EpochFail", direction="newer")
events = (
	(rev['user'], Timestamp(rev['timestamp']), rev)
	for rev in revs
)

for user_text, session in sessions.sessions(events):
	
	for event in enumerate(session):
		rev = event.data
		print(
		  "\t".join([user_text, 
		             str(i), 
		             event.timestamp.short_format(), 
		             str(rev['revid'])])
		)
	




