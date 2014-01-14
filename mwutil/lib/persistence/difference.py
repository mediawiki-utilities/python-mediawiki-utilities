from difflib import SequenceMatcher

def sequence_matcher(old, new):
	sm = SequenceMatcher(None, list(old), list(new))
	return sm.get_opcodes()

def apply(ops, old, new):
	for code, a_start, a_end, b_start, b_end in ops:
		if code   == "insert":
			for t in new[b_start:b_end]: yield t
		elif code == "replace":
			for t in new[b_start:b_end]: yield t
		elif code == "equal":
			for t in old[a_start:a_end]: yield t
		elif code == "delete":
			pass
		else:
			assert False, \
				"encounted an unrecognized operation code: " + repr(code)
