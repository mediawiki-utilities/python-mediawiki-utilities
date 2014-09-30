"""
Prints the rev_id, characters and hash of all revisions to User:EpochFail.
"""
import os
import sys

try:
    sys.path.insert(0, os.path.abspath(os.getcwd()))
    from mw import api
except:
    raise

api_session = api.Session("https://en.wikipedia.org/w/api.php")

user_docs = api_session.users.query(
    users=["EpochFail", "Halfak (WMF)"]
)

for user_doc in user_docs:
    print(user_doc)
