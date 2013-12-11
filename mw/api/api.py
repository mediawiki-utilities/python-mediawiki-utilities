import requests, traceback, sys, logging, time
from requests.exceptions import HTTPError, ConnectionError, Timeout
from requests.exceptions import TooManyRedirects

from ..util import null_or
from ..lib import api
from .recent_changes import RecentChanges

class APIError(Exception):
	
	def __init__(self, doc):
		self.doc = doc

class ErrorCode(APIError):
	
	def __init__(self, doc):
		super().__init__(self, doc)
		self.code = doc['error'].get('code')
		self.message = doc['error'].get('message')

class AuthenticationError(APIError):
	
	def __init__(self, doc):
		super().__init__(self, doc)
		self.result = doc['login']['result']
	
class MalformedResponse(APIError):
	
	def __init__(self, key, doc):
		super().__init__(self, doc)
		self.key = key

class API(api.API):
	
	def __init__(self, *args, **kwargs):
		super().__init__(self, *args, **kwargs)
		
		self.revisions = Revisions(self)
		self.recent_changes = RecentChanges(self)
		self.pages = Pages(self)
		self.user_contribs = UserContribs(self)
		self.site_info = SiteInfo(self)
	
	def login(self, username, password):
		#get token
		doc = self.post(
			self.uri,
			params={
				'action': "login",
				'lgname': username,
				'lgpassword': password,
				'format': "json"
			}
		)
		
		try:
			if doc['login']['result'] not in ("Success", "NeedToken"):
				raise AuthenticationError(doc)
			
			token = doc['login']['token']
		except KeyError() as e:
			raise MalformedResponse(e.message, doc)
		
		#try again
		doc = self.post(
			self.uri,
			{
				'action': "login",
				'lgname': username,
				'lgpassword': password
			}
		)
		
		try:
			if doc['login']['result'] not in "Success":
				raise AuthenticationError(doc)
			
			return doc
		except KeyError as e:
			raise MalformedResponse(e.message, doc)
	
	def request(self, type, params, **kwargs):
		params.update({'format': "json"})
		
		doc = super().request(self, type, params, **kwargs).json()
		
		if 'error' in doc:
			raise APIError(doc)
		
		return doc
		
	
class Collection:
	
	
	TIMESTAMP = re.compile(r"[0-9]{4}-?[0-9]{2}-?[0-9]{2}T?" + 
	                       r"[0-9]{2}:?[0-9]{2}:?[0-9]{2}Z?")
	
	DIRECTIONS = {'newer', 'older'}
	
	def _check_direction(self, direction):
		if direction == None:
			return direction
		else:
			direction = str(direction)
			
			assert direction in {None} | self.DIRECTIONS, \
				"Direction must be one of {0}".format(self.DIRECTIONS)
			
			return direction
	
	def _check_timestamp(self, timestamp):
		if timestamp == None:
			return timestamp
		else:
			timestamp = str(timestamp)
			
			if not self.TIMESTAMP.match(timestamp):
				raise TypeError("{0} is not formatted like a MediaWiki timestamp.".format(repr(timestamp))
				
			return timestamp
	
	def _items(self, items, none=True, levels=None, type=lambda val:val):
		
		if none and items == None:
			return None
		else:
			items = {str(type(item)) for item in items}
			
			if levels != None:
				levels = {str(level) for level in levels}
				
				assert len(levels - items) == 0, \
					"items {0} not in levels {1}".format(
						levels - items, levels)
				
			
			return "|".join(items)
