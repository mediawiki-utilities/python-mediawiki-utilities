.. _mw.database:

=========================================
mw.database -- MySQL database abstraction
=========================================

This module contains a set of utilities for interacting with MediaWiki databases.

Here's an example of a common usage pattern:
::
	
	from mw import database
	
	db = database.DB.from_params(
		host="s1-analytics-slave.eqiad.wmnet", 
		read_default_file="~/.my.cnf", 
		user="research", 
		db="enwiki"
	)
	revisions = db.revisions.query(user_id=9133062)
	
	for rev_row in revisions:
		rev_row['rev_id']


DB
======

.. autoclass:: mw.database.DB
   :members:
   :member-order: bysource
   

Collections
===========

.. autoclass:: mw.database.Archives
   :members:

.. autoclass:: mw.database.AllRevisions
   :members:

.. autoclass:: mw.database.Pages
   :members:

.. autoclass:: mw.database.RecentChanges
   :members:

.. autoclass:: mw.database.Revisions
   :members:

.. autoclass:: mw.database.Users
   :members: