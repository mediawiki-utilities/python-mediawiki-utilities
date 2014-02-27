============
MW Utilities
============

MW Utilities is an open source (MIT Licensed) library developed by Aaron Halfaker for extracting data from MediaWiki installations and performing some interesting computations.  A typical usage looks like this::

	from mwutil.api import API
	from mwutil.lib import reverts
	
	api = API("https://en.wikipedia.org/w/api.php")
	revs = api.revisions.query(titles=["User:EpochFail"])
	rev_events = (rev['sha1'], rev for rev in revs)
	
	for revert in reverts.reverts(rev_events):
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
``mw.lib.persistence``
	A set of utilities for tracking the persistence of content between revisions

``mw.lib.reverts``
	A set of utilities for performing revert detection

``mw.lib.sessions``
	A set of utilities for grouping revisions and other events into sessions

``mw.lib.titles``
	A set of utilities for normalizing and parsing page titles


More examples
=============
::

	from mwutil.api import API
	from mwutil.lib import sessions
	
	api = API("https://en.wikipedia.org/w/api.php")
	revs = api.user_contribs.query(user="EpochFail")
	rev_events = (rev['user'], rev['timestamp'], rev for rev in revs)
	
	for user, session in sessions.sessions(revs):
		print("{0}'s session with {1} revisions".format(user, len(session))

About the author
================
Aaron Halfaker (aaron.halfaker@gmail.com) -- http://halfaker.info -- http://en.wikipedia.org/User:EpochFail


Contributors
============
None yet.  See http://bitbucket.org/halfak/mediawiki-utilities
