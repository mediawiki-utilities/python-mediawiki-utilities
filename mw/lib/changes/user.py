from .event import Event

class Created(LogEvent):
	
	matches = [
		Match("newusers", "create", False),
		Match("newusers", "create2", False),
		Match("newusers", "byemail", False)
	]
	
	_example="""
	{
		"type": "log",
		"ns": 2,
		"title": "User:IntDebBall",
		"rcid": 616284425,
		"pageid": 0,
		"revid": 0,
		"old_revid": 0,
		"user": "IntDebBall",
		"userid": 20124261,
		"oldlen": 0,
		"newlen": 0,
		"timestamp": "2013-11-12T03:56:32Z",
		"comment": "",
		"logid": 52558177,
		"logtype": "newusers",
		"logaction": "create",
		"tags": []
	},
	{
		"type": "log",
		"ns": 2,
		"title": "User:Fredielyn Bucio",
		"rcid": 616279592,
		"pageid": 0,
		"revid": 0,
		"old_revid": 0,
		"user": "Palmville",
		"userid": 20124109,
		"oldlen": 0,
		"newlen": 0,
		"timestamp": "2013-11-12T03:19:42Z",
		"comment": "",
		"logid": 52557705,
		"logtype": "newusers",
		"logaction": "create2",
		"tags": []
	},
	{
		"type": "log",
		"ns": 2,
		"title": "User:Phillykidd",
		"rcid": 616286015,
		"pageid": 0,
		"revid": 0,
		"old_revid": 0,
		"user": "Callanecc",
		"userid": 20124315,
		"oldlen": 0,
		"newlen": 0,
		"timestamp": "2013-11-12T04:09:32Z",
		"comment": "Requested account at [[WP:ACC]], request #110880",
		"logid": 52558431,
		"logtype": "newusers",
		"logaction": "byemail",
		"tags": []
	},"""
	
	def __init__(self, user, *args, **kwargs):
		super().__init__(self, *args, **kwargs)
		
		self.user = User(user)
		
		super().register(self)
	
	@classmethod
	def from_api(self, doc):
		
		if doc['logaction'] == "create":
			name = doc['user']
		else: #doc['logaction'] in ("create2","byemail")
			ns, name_title = Page.parse_title(doc['title'])
			name = User.normalize(name_title)
		
		return cls(
			User(
				doc['userid'],
				name
			),
			doc['logid'],
			doc['rcid'],
			Timestamp(doc['timestamp']),
			doc['comment']
		)

class Renamed(LogEvent):
	
	matches = [
		Match("renameuser", "renameuser", False)
	]
	
	_example="""
	{
		"type": "log",
		"ns": 2,
		"title": "User:Tuhin Karmakar",
		"rcid": 615891880,
		"pageid": 0,
		"revid": 0,
		"old_revid": 0,
		"user": "Andrevan",
		"userid": "13732",
		"oldlen": 0,
		"newlen": 0,
		"timestamp": "2013-11-10T12:04:41Z",
		"comment": "WP:CHU",
		"logid": 52520596,
		"logtype": "renameuser",
		"logaction": "renameuser",
		"olduser": "Tuhin Karmakar",
		"newuser": "Anonymous23648762289",
		"edits": 19,
		"tags": []
	}"""
	
	def __init__(self, user, old_name, new_name, *args, **kwargs):
		super().__init__(self, *args, **kwargs)
		self.user = User(user)
		self.old_name = User.normalize(old_name)
		self.new_name = User.normalize(new_name)
		
	@classmethod
	def from_api(cls, doc):
		
		return cls(
			User(
				int(doc['userid']),
				doc['user']
			),
			doc['olduser'],
			doc['newuser'],
			doc['logid'],
			doc['rcid'],
			Timestamp(doc['timestamp']),
			doc['comment']
		)

class Blocked(Event):
	
	matches = [
		Match("block", "block", False)
	]
	
	_example="""
	{
		"type": "log",
		"ns": 2,
		"title": "User:190.203.41.111",
		"rcid": 616287367,
		"pageid": 0,
		"revid": 0,
		"old_revid": 0,
		"user": "ProcseeBot",
		"userid": "8760229",
		"bot": "",
		"oldlen": 0,
		"newlen": 0,
		"timestamp": "2013-11-12T04:21:18Z",
		"comment": "{{blocked proxy}} <!-- 8080 -->",
		"logid": 52558623,
		"logtype": "block",
		"logaction": "block",
		"block": {
			"flags": "nocreate",
			"duration": "60 days",
			"expiry": "2014-01-11T04:21:18Z"
		},
		"tags": []
	}"""
	
	def __init__(self, user, blocked_name, flags, duration, expiry, *args, **kwargs):
		super().__init__(self, *args, **kwargs)
		self.user         = User(user)
		self.blocked_name = User.normalize(blocked_name)
		self.flags        = list(flags)
		self.duration     = str(duration)
		self.expiry       = Timestamp(expiry)
		
	
	@classmethod
	def from_api(cls, doc):
		ns, title = Page.parse_title(doc['title'])
		blocked_name = User.normalize(title)
		
		return cls(
			User(
				doc['userid'],
				doc['user']
			),
			blocked_name,
			doc['block']['flags'],
			doc['block']['duration'],
			doc['block']['expiry'],
			doc['logid'],
			doc['rcid'],
			Timestamp(doc['timestamp']),
			doc['comment']
		)

class Unblocked(Event): 
	
	matches = [
		Match('block', 'unblock', False)
	]
	
	_example="""
	{
		"type": "log",
		"ns": 2,
		"title": "User:RYasmeen (WMF)",
		"rcid": 616266827,
		"pageid": 41055069,
		"revid": 0,
		"old_revid": 0,
		"user": "Risker",
		"userid": "726851",
		"oldlen": 0,
		"newlen": 0,
		"timestamp": "2013-11-12T01:48:22Z",
		"comment": "per [[https://en.wikipedia.org/wiki/User_talk:RYasmeen_%28WMF%29#Staff_account]]",
		"logid": 52556522,
		"logtype": "block",
		"logaction": "unblock",
		"tags": []
	}"""
	
	def __init__(self, user, unblocked_name, *args, **kwargs):
		super().__init__(self, *args, **kwargs)
		self.user = User(user)
		self.unblocked_name = User.normalize(unblocked)
		
	
	@classmethod
	def from_api(cls, doc):
		ns, title = Page.parse_title(doc['title'])
		unblocked_name = User.normalize(title)
		
		return cls(
			User(
				doc['userid'],
				doc['user']
			),
			unblocked_name,
			doc['logid'],
			doc['rcid'],
			Timestamp(doc['timestamp']),
			doc['comment']
		)