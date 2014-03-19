import time, logging
from itertools import chain

from ..lib import reverts
from ..types import Timestamp
from ..util import iteration

from .collection import Collection

logger = logging.getLogger("mw.database.revisions")
	
class AllRevisions:
	
	def get(self, rev_ids, include_page=False):
		rev_ids = set(int(id) for id in rev_ids)
		revisions = self.db.revisions.get(rev_ids, include_page)
		archives = self.db.archives.get(rev_ids, include_page)
		
		return chain(revisions, archives)
		
	def query(self, *args, **kwargs):
		
		revisions = self.db.revisions.query(*args, **kwargs)
		if 'include_page' in kwargs: del kwargs['include_page']
		archives = self.db.archives.query(*args, **kwargs)
		
		if 'direction' in kwargs:
			direction = kwargs['direction']
			if direction not in self.DIRECTIONS: 
				raise TypeError("direction must be in {0}".format(self.DIRECTIONS))
			
			if direction == "newer":
				collated_revisions = iteration.sequence(
					revisions, 
					archives,
					compare=lambda r1, r2: (r1['rev_timestamp'], r1['rev_id']) <= \
					               (r2['rev_timestamp'], r2['rev_id'])
				)
			else: # direction == "older"
				collated_revisions = iteration.sequence(
					revisions, 
					archives,
					compare=lambda r1, r2: (r1['rev_timestamp'], r1['rev_id']) >= \
					               (r2['rev_timestamp'], r2['rev_id'])
				)
		else:
			collated_revisions = chain(revisions, archives)
		
		if 'limit' in kwargs:
			limit = kwargs['limit']
			
			for i, rev in enumerate(collated_revisions):
				yield rev 
				if i >= limit: break
			
		else:
			for rev in collated_revisions:
				yield rev

class Revisions:
	
	def get(self, rev_ids, include_page=False):
		query = """
			SELECT *, FALSE AS archived FROM revision
		"""
		if include_page:
			query += """
				INNER JOIN page ON page_id = rev_page
			"""
		
		query += " WHERE rev_id IN ({0})".format(",".join(str(int(id)) for id in rev_ids))
		
		cursor.execute(query)
		for row in cursor:
			return row
		
	
	def query(self, page_id=None, user_id=None, 
	          before=None, after=None, before_id=None, after_id=None, 
	          direction=None, limit=None, include_page=False):
		
		start_time = time.time()
		cursor = self.db.shared_connection.cursor()
		
		query = """
			SELECT *, FALSE AS archived FROM revision
		"""
		if include_page:
			query += """
				INNER JOIN page ON page_id = rev_page
			"""
		
		query += """
			WHERE 1
		"""
		values = []
		
		if page_id != None:
			query += " AND rev_page = ? "
			values.append(int(page_id))
		if user_id != None:
			query += " AND rev_user = ? "
			values.append(int(user_id))
		if before != None:
			query += " AND rev_timestamp < ? "
			values.append(Timestamp(before).short_format())
		if after != None:
			query += " AND rev_timestamp > ? "
			values.append(Timestamp(after).short_format())
		if before_id != None:
			query += " AND rev_id < ? "
			values.append(int(before_id))
		if after_id != None:
			query += " AND rev_id > ? "
			values.append(int(after_id))
		
		
		if direction != None:
			if direction not in self.DIRECTIONS: 
				raise TypeError("direction must be in {0}".format(self.DIRECTIONS))
			
			direction = ("ASC " if direction == "newer" else "DESC ")
			query += " ORDER BY rev_timestamp {0}, rev_id {0}".format(direction)
		
		if limit != None:
			query += " LIMIT ? "
			values.append(limit)
		
		cursor.execute(query, values)
		count = 0
		for row in cursor:
			yield row
			count += 1
		
		logger.debug("%s revisions read in %s seconds" % (count, time.time() - start_time))
	


class Archives(Collection):
	
	def get(self, rev_ids):
		query = """
			SELECT
				ar_id,
				ar_rev_id AS rev_id,
				ar_page_id AS rev_page,
				ar_page_id AS page_id,
				ar_title AS page_title,
				ar_namespace AS page_namespace,
				ar_text_id AS rev_text_id,
				ar_comment AS rev_comment,
				ar_user AS rev_user,
				ar_user_text AS rev_user_text,
				ar_timestamp AS rev_timestamp,
				ar_minor_edit AS rev_minor_edit,
				ar_deleted AS rev_deleted,
				ar_len AS rev_len,
				ar_parent_id AS rev_parent_id,
				ar_sha1 AS rev_sha1,
				TRUE AS archived
			FROM archive
		"""
		
		query += " WHERE ar_rev_id IN ({0})".format(",".join(str(int(id)) for id in rev_ids))
		
		cursor.execute(query)
		for row in cursor:
			return row
		
	
	def query(self, page_id=None, user_id=None, 
	          before=None, after=None, before_id=None, after_id=None, 
	          direction=None, limit=None):
		
		start_time = time.time()
		cursor = self.db.shared_connection.cursor()
		
		query = """
			SELECT
				ar_id,
				ar_rev_id AS rev_id,
				ar_page_id AS rev_page,
				ar_page_id AS page_id,
				ar_title AS page_title,
				ar_namespace AS page_namespace,
				ar_text_id AS rev_text_id,
				ar_comment AS rev_comment,
				ar_user AS rev_user,
				ar_user_text AS rev_user_text,
				ar_timestamp AS rev_timestamp,
				ar_minor_edit AS rev_minor_edit,
				ar_deleted AS rev_deleted,
				ar_len AS rev_len,
				ar_parent_id AS rev_parent_id,
				ar_sha1 AS rev_sha1,
				TRUE AS archived
			FROM archive
		"""
		
		query += """
			WHERE 1
		"""
		values = []
		
		if page_id != None:
			query += " AND ar_page_id = ? "
			values.append(int(page_id))
		if user_id != None:
			query += " AND ar_user = ? "
			values.append(int(user_id))
		if before != None:
			query += " AND ar_timestamp < ? "
			values.append(Timestamp(before).short_format())
		if after != None:
			query += " AND ar_timestamp > ? "
			values.append(Timestamp(after).short_format())
		if before_id != None:
			query += " AND ar_rev_id < ? "
			values.append(int(before_id))
		if after_id != None:
			query += " AND ar_rev_id > ? "
			values.append(int(after_id))
		
		if direction != None:
			if direction not in self.DIRECTIONS: 
				raise TypeError("direction must be in {0}".format(self.DIRECTIONS))
			
			direction = ("ASC " if direction == "newer" else "DESC ")
			query += " ORDER BY ar_timestamp {0}, ar_rev_id {0}".format(direction)
		if limit != None:
			query += " LIMIT ? "
			values.append(limit)
		
		cursor.execute(query, values)
		count = 0
		for row in cursor:
			yield row
			count += 1
		
		logger.debug("%s revisions read in %s seconds" % (count, time.time() - start_time))
	
