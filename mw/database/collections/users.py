import logging 

from .collection import Collection

logger = logging.getLogger("mw.database.collections.users")

class Users(Collection):
	
	def get(self, user_id=None, user_name=None):
		"""
		Gets a single user row from the database.  Raises a :class:`KeyError`
		if a user cannot be found.
		
		:Parameters:
			user_id : int
				User ID
			user_name : str
				User's name
			
		:Returns:
			A user row. 
		"""
		user_id = none_or(user_id, int)
		user_name = none_or(user_name, str)
		
		query = """
		SELECT user.*
		FROM user
		"""
		values = []
		
		if user_id != None:
			query += """
				WHERE user_id = ?
			"""
			values.append(user_id)
		
		elif user_name != None:
			query += """
				WHERE user_name = ({0})
			""".format(user_name)
		
		else:
			raise TypeError("Must specify a user identifier.")
		
		cursor = self.db.shared_connection.cursor()
		cursor.execute(
			query,
			values
		)
		
		for row in cursor:
			return row
		
		raise KeyError(user_id if user_id != None else user_name)
