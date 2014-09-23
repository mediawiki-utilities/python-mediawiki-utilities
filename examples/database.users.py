"""

"""
import os
import sys

try:
    
    sys.path.insert(0, os.path.abspath(os.getcwd()))
    from mw import database
    
except:
    raise



db = database.DB.from_params(
    host="analytics-store.eqiad.wmnet",
    read_default_file="~/.my.cnf",
    user="research",
    db="enwiki"
)

users = db.users.query(
    registered_after="20140101000000",
    direction="newer",
    limit=10
)

for user in users:
    print("{user_id}:{user_name} -- {user_editcount} edits".format(**user))
