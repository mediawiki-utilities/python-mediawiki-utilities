============
MW Utilities
============

MW Utilities is an open source (MIT Licensed) library developed by Aaron Halfaker for extracting data from MediaWiki installations and performing some interesting computations.  A typical usage looks like this::

	from mwutil.api import API
	from mwutil.lib import reverts
	
	# Gather a page's revisions from the API
	api = API("https://en.wikipedia.org/w/api.php")
	revs = api.revisions.query(titles=["User:EpochFail"])
	rev_events = (rev['sha1'], rev for rev in revs)
	
	# Detect and print revert info
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
Timestamp handling::
	
	from mwutil.types import Timestamp
	
	# Seconds since Unix Epoch
	str(Timestamp(1234567890))
	# > '20090213233130'
	
	# Database format
	int(Timestamp("20090213233130"))
	# > 1234567890
	
	# API format
	int(Timestamp("2009-02-13T23:31:30Z"))
	# > 1234567890
	
	# Difference in seconds
	Timestamp("2009-02-13T23:31:31Z") - Timestamp(1234567890)
	# > 1
	
	# strptime and strftime
	Timestamp(1234567890).strftime("%Y foobar")
	# > '2009 foobar'
	
	str(Timestamp.strptime("2009 derp 10", "%Y derp %m"))
	# > '20091001000000'
	
	

Session clustering::

	from mwutil.api import API
	from mwutil.lib import sessions
	
	# Gather a user's revisions from the API
	api = API("https://en.wikipedia.org/w/api.php")
	revs = api.user_contribs.query(user="EpochFail")
	rev_events = (rev['user'], rev['timestamp'], rev for rev in revs)
	
	# Extract and print sessions
	for user, session in sessions.sessions(revs):
		print("{0}'s session with {1} revisions".format(user, len(session))

Title normalization & parsing::
	
	from mwutil.api import API
	from mwutil.lib import title
	
	# Normalize titles
	title.normalize("foo bar")
	# > "Foo_bar"
	
	# Construct a namespace parser from the API
	api = API("https://en.wikipedia.org/w/api.php")
	si_doc = api.site_info.query(properties=['namespaces', 'namespacealiases'])
	namespaces = title.Namespaces.from_site_info(si_doc)
	
	# Handles normalization
	namespaces.parse("user:epochFail")
	# > 2, "EpochFail"
	
	# Handles namespace aliases
	namespaces.parse("WT:foobar")
	# > 5, "Foobar"
	
Dump iteration::
	
	from mwutil import dump
	
	# Construct dump file iterator
	dump_processor = dump.Processor.from_file(open("dump.xml"))
	
	# Iterate through pages
	for page in dump_processor:
		
		# Iterate through a page's revisions
		for revision in page:
			
			print(revision.id)
		
	


About the author
================
Aaron Halfaker (aaron.halfaker@gmail.com) -- http://halfaker.info -- http://en.wikipedia.org/User:EpochFail


Contributors
============
None yet.  See http://bitbucket.org/halfak/mediawiki-utilities
