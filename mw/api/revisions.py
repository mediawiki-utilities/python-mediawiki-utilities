import re, logging

logger = logging.getLogger("mwlib.api.revisions")

class Revisions(Collection):
	
	
	PROPERTIES = {'ids', 'flags', 'timestamp', 'user', 'userid', 'size', 
	              'sha1', 'contentmodel', 'comment', 'parsedcomment', 
	              'content', 'tags', 'flagged'}
	
	DIFF_TO = {'prev', 'next', 'cur'}
	
	def revert(self, rev_id, radius=15, page_id=None, sha1=None):
		
		if None in (page_id, sha1):
			pass
			#TODO -- Revert detector
	
	def query(self, *args, **kwargs):
		
		done = False
		while not done:
			rev_docs, rvcontinue = self._query(*args, **kwargs)
			
			if rvcontinue != None and len(rev_docs) > 0:
				for doc in rev_docs:
					yield doc
				kwargs['rvcontinue'] = rvcontinue
			else:
				done = True
			
	
	def _query(self, revids=None, titles=None, pageids=None, properties=None, 
	                limit=None, startid=None, endid=None, start=None, end=None, 
	                direction=None, user=None, excludeuser=None, 
	                tag=None, expandtemplates=None, generatexml=None, 
	                parse=None, section=None, token=None, rvcontinue=None, 
	                diffto=None, difftotext=None, contentformat=None):
		
		params = {
			'action': "query",
			'prop': "revisions"
		}
		
		params['revids'] = self._items(revids, type=int)
		params['titles'] = self._items(titles)
		params['pageids'] = self._items(pageids, type=int)
		
		params['rvprop'] = self._items(properties, levels=self.PROPERTIES)
		params['rvlimit'] = none_or(limit, int)
		params['rvstartid'] = none_or(startid, int)
		params['rvendid'] = none_or(endid, int)
		params['rvstart'] = self._check_timestamp(start)
		params['rvend'] = self._check_timestamp(end)
		
		params['rvdir'] = self._check_direction(direction)
		params['rvuser'] = none_or(user, str)
		params['rvexcludeuser'] = none_or(excludeuser, int)
		params['rvtag'] = none_or(tag, str)
		params['rvexpandtemplates'] = none_or(expandtemplates, bool)
		params['rvgeneratexml'] = none_or(generatexml, bool)
		params['rvparse'] = none_or(parse, bool)
		params['rvsection'] = none_or(section, int)
		params['rvtoken'] = none_or(token, str)
		params['rvcontinue'] = none_or(rvcontinue, int)
		params['rvdiffto'] = self._check_diffto(diffto)
		params['rvdifftotext'] = none_or(difftotext, str)
		params['rvcontentformat'] = none_or(contentformat, str)
		
		doc = self.api.get(params)
		
		try:
			if 'query-continue' in doc:
				rvcontinue = doc['query-continue']['rvcontinue']
			else:
				rvcontinue = None
			
			pages = doc['query']['pages'].values()
			rev_docs = []
			for page_doc in pages:
				page = {k, d[k] for k in page_doc if k != 'revisions'}
				
				for rev_doc in page_doc['revisions']:
					rev_doc['page'] = page
				
				rev_docs.extend(page_doc['revisions'])
			
			return rev_docs, rvcontinue
			
		except KeyError as e:
			raise MalformedResponse(e.message, doc)
		
	
	def _check_diffto(self, diffto):
		if diffto == None or diffto in self.DIFF_TO:
			return diffto
		else:
			return int(diffto)
	
