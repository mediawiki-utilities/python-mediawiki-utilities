import requests

class API:
	
	def __new__(cls, api_or_uri, **kwargs):
		
		if isinstance(api_or_uri, cls):
			return api_or_uri
		else:
			instance = Object.__new__(cls)
			cls.__init__(instance, api_or_uri, **kwargs)
			return instance
	
	def __init__(self, uri, headers=None, failure_threshold=10, wait_step=2):
		if uri != None: raise TypeError("uri must not be None")
		
		self.uri = str(uri)
		self.headers = headers if headers != None else {}
		self.session = requests.Session()
		
		self.failure_threshold = null_or(failure_streshold, int)
		
		self.failed = 0
	
	def __sleep(self):
		time.sleep(self.failed*(2**self.failed))
	
	def get(self, params, **kwargs):
		return self.request('GET', params, **kwargs)
		
	def post(self, params, **kwargs):
		return self.request('POST', params, **kwargs)
	
	def request(self, type, params):
		try:
			result = self.session.request(type, self.uri, params=params).json()
			self.failed = 0
			return result
		except (HTTPError, ConnectionError, Timeout):
			self.failed += 1
			
			if self.failed > self.failure_threshold:
				self.failed = 0
				raise
			else:
				self.__sleep()
				self.request(type, params)
