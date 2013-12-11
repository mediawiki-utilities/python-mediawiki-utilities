
from .db import Collection

class Pages(Collection):
	def get_page(self, rev_id):
		cursor = self.db.shared_connection.cursor()
		cursor.execute(
			"""
			SELECT page_id, page_title, page_namespace
			FROM page
			INNER JOIN revision ON rev_page = page_id
			WHERE rev_id = ?
			""",
			(rev_id,)
		)
		
		for row in cursor:
			return row
		
		raise KeyError(rev_id)
