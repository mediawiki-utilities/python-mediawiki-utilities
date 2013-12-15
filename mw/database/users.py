import logging 

from .collection import Collection

logger = logging.getLogger("mw.database.users")

class Users(Collection):
	def get(self, user_id=None, user_name=None):
		
		query = """
		SELECT user.*
		FROM user
		"""
		values = []
		
		if user_id != None:
			query += """
				WHERE user_id = ?
			"""
			values.append(int(user_id))
		
		elif user_name != None:
			query += """
				WHERE user_name = ({0})
			""".format(str(user_name))
		
		else:
			raise TypeError("Must specify a user identifier.")
		
		cursor = self.db.shared_connection.cursor()
		cursor.execute(
			query,
			values
		)
		
		for row in cursor:
			return row
