class Parser:
	
	def __init__(self, namespaces):
		self.namespaces = Namespaces(namespaces)
		
	def parse(page_name):
		parts = page_name.split(":", 1)
		if len(parts) == 1:
			ns_id = 0
			title = normalize(page_name)
		else:
			ns_name, title = parts
			ns_name, title = normalize(ns_name), normalize(ns_title)
			
			if ns_name in self.namespaces:
				ns_id = self.namespaces.get(name=ns_name).id
			else:
				ns_id = 0
				title = normalize(page_name)
			
		
		return ns_id, title
