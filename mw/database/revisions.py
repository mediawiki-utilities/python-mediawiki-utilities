class Revisions:
	
	def __init__(self, db):
		self.db = db
	
	def query(self, page_id=None, user_id=None, 
		before=None, after=None, before_id=None, after_id=None, 
		dir="newer", limit=None):
		start_time = time.time()
		cursor = self.db.shared_connection.cursor()
		
		query = """
			SELECT * FROM revision
			INNER JOIN page ON page_id = rev_page
			WHERE 1
		"""
		fields = []
		
		if page_id != None:
			query += " AND rev_page = ? "
			fields.append(page_id)
		if user_id != None:
			query += " AND rev_user = ? "
			fields.append(user_id)
		if before != None:
			query += " AND rev_timestamp < ? "
			fields.append(before)
		if after != None:
			query += " AND rev_timestamp > ? "
			fields.append(after)
		if before_id != None:
			query += " AND rev_id < ? "
			fields.append(before_id)
		if after_id != None:
			query += " AND rev_id > ? "
			fields.append(after_id)
		
		query += " ORDER BY rev_id " + ("ASC " if dir == "newer" else "DESC ")
		
		if limit != None:
			query += " LIMIT ? "
			fields.append(limit)
		
		cursor.execute(query, tuple(fields))
		count = 0
		for row in cursor:
			yield row
			count += 1
		
		logger.debug("%s revisions read in %s seconds" % (count, time.time() - start_time))
	
	def revert(self, rev, radius=15, before=None):
		
		# Prepare history
		history = {}
		
		# Load history
		past_revs = list(self.query(
			page_id=rev['page_id'],
			radius=5,
			before_id=rev['rev_id'],
			dir='older'
		))
		for prev in reversed(past_revs):
			history[prev['rev_sha1']] = prev
		
		
		# Check future
		future_revs = self.query(
			page_id=rev['page_id'],
			radius=5,
			after_id=rev['rev_id'],
			before=before,
			dir='newer'
		)
		for frev in future_revs:
			if frev['rev_sha1'] == rev['rev_sha1']:
				# Noop
				pass
			elif frev['rev_sha1'] in history:
				# Revert
				return frev
			
		return None

