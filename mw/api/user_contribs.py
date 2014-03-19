import re, logging

from ..util import none_or

from .collection import Collection
from .errors import MalformedResponse

logger = logging.getLogger("mwlib.api.user_contribs")

class UserContribs(Collection):
	
	
	PROPERTIES = {'ids', 'title', 'timestamp', 'comment', 'parsedcomment', 
	              'size', 'sizediff', 'flags', 'patrolled', 'tags'}
	
	SHOW = {'minor', '!minor', 'patrolled', '!patrolled'}
	
	UCCONTINUE = re.compile(r"[A-Z0-9]|[0-9]{4}-[0-9]{2}-[0-9]{2}T" + 
	                        r"[0-9]{2}:[0-9]{2}:[0-9]{2}Z")
	
	def _check_uccontinue(self, rccontinue):
		if rccontinue == None:
			return None
		elif self.UCCONTINUE.match(rccontinue):
			return rccontinue
		else:
			raise TypeError(
				"uccontinue {0} is not formatted correctly ".format(rccontinue) + \
				"'%Y-%m-%dT%H:%M:%SZ|<last_rcid>'"
			)
	
	def query(self, *args, **kwargs):
		
		done = False
		while not done:
			uc_docs, uccontinue = self._query(*args, **kwargs)
			
			for doc in uc_docs:
				yield doc
			
			if uccontinue == None or len(uc_docs) == 0: 
				done = True
			else:
				kwargs['uccontinue'] = uccontinue
	
	
	def _query(self, user=None, userprefix=None, limit=None, start=None, 
	                end=None, direction=None, namespace=None, properties=None, 
	                show=None, tag=None, toponly=None,
	                uccontinue=None):
		
		params = {
			'action': "query",
			'list': "usercontribs"
		}
		params['uclimit'] = none_or(limit, int)
		params['ucstart'] = self._check_timestamp(start)
		params['ucend'] = self._check_timestamp(end)
		params['uccontinue'] = self._check_uccontinue(uccontinue)
		params['ucuser'] = self._items(user, type=str)
		params['ucuserprefix'] =  self._items(userprefix, type=str)
		params['ucdir'] = self._check_direction(direction)
		params['ucnamespace'] = none_or(namespace, int)
		params['ucprop'] = self._items(properties, levels=self.PROPERTIES)
		params['ucshow'] = self._items(show, levels=self.SHOW)
		
		doc = self.session.get(params)
		try:
			if 'query-continue' in doc:
				uccontinue = doc['query-continue']['usercontribs']['uccontinue']
			else:
				uccontinue = None
			
			uc_docs = doc['query']['usercontribs']
			
			return uc_docs, uccontinue
			
		except KeyError as e:
			raise MalformedResponse(str(e), doc)

