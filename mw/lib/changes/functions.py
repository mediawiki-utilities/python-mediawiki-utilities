from . import change

def from_api(rc_docs):
	
	for rc_doc in rc_doc:
		c = change.from_api(rc_row)
		if c != None: yield c
	
def from_db(rc_rows):
	
	for rc_row in rc_row:
		c = change.from_db(rc_row)
		if c != None: yield c
