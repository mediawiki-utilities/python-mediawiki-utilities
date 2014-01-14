class APIError(Exception):
	
	def __init__(self, doc):
		self.doc = doc

class ErrorCode(APIError):
	
	def __init__(self, doc):
		super().__init__(doc)
		self.code = doc['error'].get('code')
		self.message = doc['error'].get('message')

class AuthenticationError(APIError):
	
	def __init__(self, doc):
		super().__init__(doc)
		self.result = doc['login']['result']
	
class MalformedResponse(APIError):
	
	def __init__(self, key, doc):
		super().__init__(doc)
		self.key = key
