def normalize(title):
	if title == None: 
		return title
	else:
		if len(title) > 0:
			return (title[0].upper() + title[1:]).replace(" ", "_")
		else:
			return ""
