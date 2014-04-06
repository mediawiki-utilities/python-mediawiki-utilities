import re, logging, sys

from ..util import none_or
from .collection import Collection
from .errors import MalformedResponse

logger = logging.getLogger("mw.api.deletedrevs")

class DeletedRevs(Collection):
	
	
	PROPERTIES = {'revid', 'parentid', 'user', 'userid', 'comment', 
	              'parsedcomment', 'minor', 'len', 'sha1', 'content', 'token', 
	              'tags'}
	
	# TODO: 
	# This is *not* the right way to do this, but it should work for all queries.
	MAX_REVISIONS = 500
	
	def query(self, *args, limit=sys.maxsize, **kwargs):
		# `limit` means something diffent here
		kwargs['limit'] = min(limit, self.MAX_REVISIONS)
		revisions_yielded = 0
		done = False
		while not done and revisions_yielded <= limit:
			rev_docs, drcontinue = self._query(*args, **kwargs)
			for doc in rev_docs:
				yield doc
				revisions_yielded += 1
				if revisions_yielded >= limit: break
				
			if drcontinue != None and len(rev_docs) > 0:
				kwargs['drcontinue'] = drcontinue
			else:
				done = True
			
	
	def _query(self, titles=None,
	                 start=None, end=None, from_title=None, to_title=None, 
	                 prefix=None, drcontinue=None, unique=None, tag=None,
	                 user=None, excludeuser=None, namespace=None, limit=None,
	                 properties=None, direction=None):
		
		params = {
			'action': "query",
			'list': "deletedrevs"
		}
		
		params['titles'] = self._items(titles)
		params['drprefix'] = none_or(prefix, str)
		params['drfrom'] = none_or(from_title, str)
		params['drto'] = none_or(to_title, str)
		
		params['drprop'] = self._items(properties, levels=self.PROPERTIES)
		params['drlimit'] = none_or(limit, int)
		params['drstart'] = self._check_timestamp(start)
		params['drend'] = self._check_timestamp(end)
		
		params['drdir'] = self._check_direction(direction)
		params['druser'] = none_or(user, str)
		params['drexcludeuser'] = none_or(excludeuser, int)
		params['drtag'] = none_or(tag, str)
		params['drcontinue'] = none_or(drcontinue, str)
		
		doc = self.session.get(params)
		
		try:
			if 'query-continue' in doc:
				drcontinue = doc['query-continue']['deletedrevs']['drcontinue']
			else:
				drcontinue = None
			
			pages = doc['query']['deletedrevs']
			rev_docs = []
			
			for page_doc in pages:
				page_rev_docs = page_doc['revisions']
				del page_doc['revisions']
				
				for rev_doc in page_rev_docs:
					rev_doc['page'] = page_doc
				
				rev_docs.extend(page_rev_docs)
			
			return rev_docs, drcontinue
			
		except KeyError as e:
			print(doc)
			raise MalformedResponse(str(e), doc)
	
