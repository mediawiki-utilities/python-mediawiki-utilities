import requests, traceback, sys, logging, time
from requests.exceptions import HTTPError, ConnectionError, Timeout
from requests.exceptions import TooManyRedirects

from ..util import none_or, api
from .pages import Pages
from .recent_changes import RecentChanges
from .revisions import Revisions
from .site_info import SiteInfo
from .user_contribs import UserContribs

class Session(api.Session):
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		self.pages = Pages(self)
		self.revisions = Revisions(self)
		self.recent_changes = RecentChanges(self)
		self.pages = Pages(self)
		self.site_info = SiteInfo(self)
		self.user_contribs = UserContribs(self)
	
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
		
		doc = super().request(type, params, **kwargs).json()
		
		if 'error' in doc:
			raise APIError(doc)
		
		return doc
		
	

