
from ..types import Timestamp

from .collection import Collection

class RecentChanges:
	
	 # (https://www.mediawiki.org/wiki/Manual:Recentchanges_table)
	TYPES = {
		'edit': 0, # edit of existing page
		'new': 1, # new page
		'move': 2, # Marked as obsolete 
		'log': 3, # log action (introduced in MediaWiki 1.2)
		'move_over_redirect': 4, # Marked as obsolete 
		'external': 5 # An external recent change. Primarily used by Wikidata
	}
	
	def query(self, before=None, after=None, before_id=None, after_id=None, 
	                types=None, direction=None, limit=None):
		
		query = """
			SELECT * FROM recentchanges
			WHERE 1
		"""
		values = []
		
		if before != None:
			query += " AND rc_timestamp < ? "
			values.append(Timestamp(before).short_format())
		if after != None:
			query += " AND rc_timestamp < ? "
			values.append(Timestamp(after).short_format())
		if before_id != None:
			query += " AND rc_id < ? "
			values.append(int(before_id))
		if after_id != None:
			query += " AND rc_id < ? "
			values.append(int(after_id))
		if types != None:
			types = set(str(t) for t in types)
			non_types = types - self.TYPES.keys()
			if len(non_types) > 0:
				raise TypeError("types must be a set of values from {0}".format(self.KEYS)
			query += " AND rc_type IN ({0}) ".format(
				",".join(self.TYPES[t] for t in types)
			)
		
		
		if direction != None:
			if direction not in self.DIRECTIONS: 
				raise TypeError("direction must be in {0}".format(self.DIRECTIONS))
			
			dir = ("ASC " if dir == "ASC" else "DESC ")
			query += " ORDER BY rc_timestamp {0}, rc_id {0}".format(dir)
		
		if limit != None:
			query += " LIMIT ? "
			values.append(limit)
		
		cursor.execite(query, values)
		for row in cursor:
			yield row
