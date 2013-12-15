"""
Prints the ids and usernames of newly registered users updated based on renames.
"""
from mw.lib import events
from mw.api import API

api = API("https://en.wikipedia.org/w/api.php")

rccontinue = "|".join(Timestamp(0).long_format(), str(0))

rc_docs = api.recent_changes.query(direction="newer", rccontinue=rccontinue)

names = {}

for event in events.from_api(rc_docs):
	
	if isinstance(event, events.user.New):
		names[event.user.name] = event.user.id
	elif isinstance(event, events.user.Renamed):
		if event.old_name in names:
			id = names[event.old_name] # Get old id
			del names[event.old_name] # Remove old name record
			names[event.new_name] = id # Record new name record
		
	

for name, id in names.items():
	print("\t".join([str(id), name])

