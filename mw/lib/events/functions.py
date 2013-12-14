
def events_from_api(rc_docs):
	
	for rc_doc in rc_doc:
		yield Event.from_api(rc_doc)
