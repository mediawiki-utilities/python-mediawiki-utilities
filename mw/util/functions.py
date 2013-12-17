def none_or(val, f, levels=None):
	if val == None:
		return None
	else:
		if levels != None and val in set(levels):
			return val
		else:
			return f(val)
