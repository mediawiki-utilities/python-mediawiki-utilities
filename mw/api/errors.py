class APIError(Exception):
	
	def __init__(self, message, doc):
		super().__init__(message)
		self.doc = doc

class ErrorCode(APIError):
	
	def __init__(self, doc):
		code = doc['error'].get('code')
		message = doc['error'].get('message')
		
		super().__init__("{0}:{1}".format(code, message), doc)
		self.code = code
		self.message = message
		


class AuthenticationError(APIError):
	
	def __init__(self, doc):
		result = doc['login']['result']
		super().__init__(result, doc)
		
		self.result = result
	
class MalformedResponse(APIError):
	
	def __init__(self, key, doc):
		super().__init__(key, doc)
		self.key = key
