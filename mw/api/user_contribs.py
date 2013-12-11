import re, logging

logger = logging.getLogger("mwlib.api.user_contribs")

class UserContribs(Collection):
	
	
	PROPERTIES = {'ids', 'title', 'timestamp', 'comment', 'parsedcomment', 
	              'size', 'sizediff', 'flags', 'patrolled', 'tags'}
	
	SHOW = {'minor', '!minor', 'patrolled', '!patrolled'}
	
	
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
		params['uccontinue'] = self._check_timestamp(uccontinue)
		params['ucuser'] = self._items(user, type=str)
		params['ucuserprefix'] =  self._items(userprefix, type=str)
		params['ucdir'] = self._check_direction(direction)
		params['ucnamespace'] = none_of(namespace, int)
		params['ucprop'] = self._items(properties, levels=self.PROPERTIES)
		params['ucshow'] = self._items(show, levels=self.SHOW)
		
		doc = self.api.query(params)
		
		try:
			contribs_docs = doc['query']['usercontribs']
			

