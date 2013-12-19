============
MW Utilities
============

MW Utilities is an open source (MIT Licensed) library developed by Aaron Halfaker for extracting data from MediaWiki installations and performing some interesting computations.  A typical usage looks like this::

	from mw.api import API
	from mw.lib import reverts
	
	api = API("https://en.wikipedia.org/w/api.php")
	revs = api.revisions.query(titles=["User:EpochFail"])
	
	for revert in reverts.reverts(revs):
		print("{0} reverted back to {1}".format(rev['revid'],
		                                        revert.revert_to['revid'])


Core modules
============
``mw.api``
	A set of utilities for interacting with MediaWiki's web API.

``mw.database``
	A set of utilities for interacting with MediaWiki's database.

``mw.dump``
	A set of utilities for interacting with MediaWiki's XML database dumps.

``mw.types``
	A set of types for working with MediaWiki data.


Libraries
=========
``mw.lib.events``
	A set of utilities for converting Recentchanges to conceptual events

``mw.lib.persistence``
	A set of utilities for tracking the persistence of content between revisions

``mw.lib.reverts``
	A set of utilities for performing revert detection

``mw.lib.sessions``
	A set of utilities for grouping revisions and other events into sessions

``mw.lib.titles``
	A set of utilities for normalizing and parsing page titles


Scripts and examples
====================
Coming soon...


About the author
================
Aaron Halfaker (aaron.halfaker@gmail.com) -- http://halfaker.info


Contributors
============
None yet.  See http://bitbucket.org/halfak/mediawiki
