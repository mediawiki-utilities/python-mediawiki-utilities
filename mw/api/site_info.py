import re, logging

logger = logging.getLogger("mwlib.api.site_info")

class SiteInfo(Collection):
	
	
	PROPERTIES = {'general', 'namespaces', 'namespacealiases', 
	              'specialpagealiases', 'magicwords', 'interwikimap', 
	              'dbrepllag', 'statistics', 'usergroups', 'extensions', 
	              'fileextensions', 'rightsinfo', 'languages', 'skins', 
	              'extensiontags', 'functionhooks', 'showhooks', 
	              'variables', 'protocols'}
	
	FILTERIW = {'local', '!local'}
	
	
	def query(self, properties=None, filteriw=None, showalldb=None, 
	               numberinggroup=None, inlanguagecode=None):
		
		siprop = self._items(properties, levels=self.PROPERTIES)
		
		doc = self.api.get(
			{
				'action': "query",
				'meta': "siteinfo",
				'siprop': siprop,
				'sifilteriw': filteriw,
				'sishowalldb': showalldb,
				'sinumberinggroup': numberinggroup,
				'siinlanguagecode': inlanguagecode
			}
		)
		
		try:
			return doc['query']
		except KeyError as e:
			raise MalformedResponse(e.message, doc)
			
