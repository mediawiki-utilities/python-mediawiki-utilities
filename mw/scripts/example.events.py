from mwlib import events
from mwlib.types import Timestamp

'''
en_api.recent_changes.list(
	start,
	end,
	dir,
	namespace,
	user,
	excludeuser,
	tag,
	properties,
	token,
	show,
	limit,
	type.
	toponly,
	query_continue,
)
'''

def read_events(api, last_time=None, last_id=None):
	last_time = last_time if last_time else Timestamp(epoch_seconds=0)
	last_id = last_id if last_id else 0
	
	while True:
		
		rc_docs = api.recent_changes.query(
			direction="newer",
			position="|".join(ts.mw_long(), 0),
			auto_continue=True
		)
		
		for rc_doc in rc_docs:
			yield events.Event.from_api(rc_doc)
		

def main():
	api = API("https://en.wikipedia.org/w/api.php")
	
	for event in read_events(api):
		
		if isinstance(event, events.page.Revised):
			# add revision
		elif isinstance(event, events.user.Renamed):
			# rename user
		

