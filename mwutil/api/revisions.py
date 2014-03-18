import re, logging, sys

from ..util import none_or
from .collection import Collection
from .errors import MalformedResponse

logger = logging.getLogger("mwlib.api.revisions")

class Revisions(Collection):
	
	
	PROPERTIES = {'ids', 'flags', 'timestamp', 'user', 'userid', 'size', 
	              'sha1', 'contentmodel', 'comment', 'parsedcomment', 
	              'content', 'tags', 'flagged'}
	
	DIFF_TO = {'prev', 'next', 'cur'}
	
	# This is *not* the right way to do this, but it should work for all queries.
	MAX_REVISIONS = 50
	
	def revert(self, rev, radius=15, before=None):
		"""
		Note that rev must contain 'page' and 'sha1'.
		"""
		
		# Load history
		past_revs = reversed(list(self.query(
			pageids=rev['page']['id'],
			limit=radius,
			before_id=rev['revid'],
			direction="older"
		)))
		future_revs = self.query(
			page_id=rev['page']['id'],
			limit=radius,
			after_id=rev['revid'],
			before=before,
			direction="newer"
		)
		checksum_revisions = ((rev['sha1'], rev)
		                      for rev in chain(past_revs, [rev], future_revs))
		
		for reverting, reverteds, reverted_to in reverts.reverts(checksum_revisions, radius=radius):
			if rev['id'] in {r['id'] for r in reverteds}:
				return revert
			
		return None
	
	def query(self, *args, limit=sys.maxsize, **kwargs):
		# `limit` means something diffent here
		kwargs['limit'] = min(limit, self.MAX_REVISIONS)
		revisions_yielded = 0
		done = False
		while not done and revisions_yielded <= limit:
			rev_docs, rvcontinue = self._query(*args, **kwargs)
			for doc in rev_docs:
				yield doc
				revisions_yielded += 1
				if revisions_yielded >= limit: break
				
			if rvcontinue != None and len(rev_docs) > 0:
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
		
		doc = self.session.get(params)
		
		try:
			if 'query-continue' in doc:
				rvcontinue = doc['query-continue']['revisions']['rvcontinue']
			else:
				rvcontinue = None
			
			pages = doc['query']['pages'].values()
			rev_docs = []
			
			for page_doc in pages:
				if 'missing' in page_doc: continue
				
				page_rev_docs = page_doc['revisions']
				del page_doc['revisions']
				
				for rev_doc in page_rev_docs:
					rev_doc['page'] = page_doc
				
				rev_docs.extend(page_rev_docs)
			
			return rev_docs, rvcontinue
			
		except KeyError as e:
			raise MalformedResponse(str(e), doc)
		
	
	def _check_diffto(self, diffto):
		if diffto == None or diffto in self.DIFF_TO:
			return diffto
		else:
			return int(diffto)
	
