import sys,os;sys.path.insert(0, os.path.abspath(os.getcwd()))
"""
Prints the rev_id, characters and hash of all revisions to User:EpochFail.
"""
from mw import database

db = database.DB.from_params(
    host = "s1-analytics-slave.eqiad.wmnet",
    read_default_file = "~/.my.cnf",
    user = "research",
    db = "enwiki"
)

users = db.users.query(
    registered_after = "20140101000000",
    registered_before = "20140101115959",
    direction = "newer",
    limit = 10
)

for user in users:
    print("{user_id}:{user_name} -- {user_editcount} edits".format(**user))
