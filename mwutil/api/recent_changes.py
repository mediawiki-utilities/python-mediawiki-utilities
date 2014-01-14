import re, logging

from .collection import Collection
from .errors import MalformedResponse

logger = logging.getLogger("mwlib.api.recent_changes")

class RecentChanges(Collection):
	
	RCCONTINUE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T" + 
	                        r"[0-9]{2}:[0-9]{2}:[0-9]{2}Z" + 
	                        r"\|[0-9]+")
	
	PROPERTIES = {'user', 'userid', 'comment', 'timestamp', 'title',
	              'ids', 'sizes', 'redirect', 'flags', 'loginfo', 
	              'tags', 'sha1'}
	
	SHOW = {'minor', '!minor', 'bot', '!bot', 'anon', '!anon', 
	        'redirect', '!redirect', 'patrolled', '!patrolled'}
	
	DIRECTIONS = {'newer', 'older'}
	
	def _check_rccontinue(self, rccontinue):
		if rccontinue == None:
			return None
		elif self.RCCONTINUE.match(rccontinue):
			return rccontinue
		else:
			raise TypeError(
				"rccontinue {0} is not formatted correctly ".format(rccontinue) + \
				"'%Y-%m-%dT%H:%M:%SZ|<last_rcid>'"
			)
	
	def query(self, *args, **kwargs):
		
		done = False
		while not done:
			rc_docs, rccontinue = self._query(*args, **kwargs)
			
			if rvcontinue != None and len(rev_docs) > 0:
				for doc in rc_docs:
					yield doc
				kwargs['rccontinue'] = rccontinue
			else:
				done = True
			
	
	def _query(self, start=None, end=None, direction=None, namespace=None, 
	                 user=None, excludeuser=None, tag=None, properties=None, 
	                 token=None, show=None, limit=None, type=None, 
	                 toponly=None, rccontinue=None):
		
		params = {
			'action': "query",
			'list':   "recentchanges"
		}
		
		params['rcstart'] = none_or(start, str)
		params['rcend'] = none_or(end, str)
		
		assert direction in {None} | self.DIRECTIONS, \
			"Direction must be one of {0}".format(self.DIRECTIONS)
		
		params['rcdir'] = direction
		params['rcnamespace'] = none_or(namespace, int)
		params['rcuser'] = none_or(user, str)
		params['rcexcludeuser'] = none_or(excludeuser, str)
		params['rctag'] = none_or(tag, str)
		params['rcprop'] = self._items(properties, levels=self.PROPERTIES)
		params['rctoken'] = none_or(tag, str)
		params['rcshow'] = self._items(show, levels=self.SHOW)
		params['rclimit'] = none_or(limit, int)
		params['rctype'] = none_or(type, str)
		params['rctoponly'] = none_or(toponly, bool)
		params['rccontinue'] = self._check_rccontinue(rccontinue)
		
		doc = self.session.get(params)
		
		try:
			rc_docs = doc['query']['recentchanges']
			
			if 'query-continue' in doc:
				rccontinue = doc['query-continue']['rccontinue']
			elif len(rc_docs) > 0:
				rccontinue = "|".join(rc_docs[-1]['timestamp'],
				                      rc_docs[-1]['rcid']+1)
			else:
				pass # Leave it be
		
		except KeyError as e:
			raise MalformedResponse(str(e), doc)
		
		
		return rc_docs, rccontinue
	
