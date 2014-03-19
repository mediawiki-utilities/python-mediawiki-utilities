import logging

from .collection import Collection

logger = logging.getLogger("mw.database.pages")

class Pages(Collection):
	def get(self, namespace=None, title=None, rev_id=None, page_ids=None):
		"""
		Gets a single page based on a legitimate identifier of the page.  Note 
		that namespace and title must be provided together.
		
		:Parameters:
			namespace : int
				the page's namespace
			title : str
				the page's title (namespace excluded)
			
		"""
		
		query = """
		SELECT page.*
		FROM page
		"""
		values = []
		
		if namespace != None or title != None:
			if title == None:
				raise TypeError("namespace and title must be specified together")
			if namespace == None:
				raise TypeError("namespace and title must be specified together")
			
			query += " WHERE page_namespace = ? and page_title = ? "
			values.extend([int(namespace), str(title)])
		
		elif rev_id != None:
			query += """
				INNER JOIN revision ON rev_page = page_id
				WHERE rev_id = ?
			"""
			values.append(int(rev_id))
		
		elif page_ids != None:
			query += """
				WHERE page_ids = ({0})
			""".format(",".join(str(int(id)) for id in page_ids))
			values.append(int(id))
		
		else:
			raise TypeError("Must specify a page identifier.")
		
		cursor = self.db.shared_connection.cursor()
		cursor.execute(
			query,
			values
		)
		
		for row in cursor:
			return row
