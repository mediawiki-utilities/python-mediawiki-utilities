============
MW Utilities
============

MediaWiki Utilities is an open source (MIT Licensed) library developed by Aaron Halfaker for extracting and processing data from MediaWiki installations, slave databses and xml dumps.

This library requires Python 3 or later.

A typical usage looks like this::

	from mw.api import Session
	from mw.lib import reverts
	
	# Gather a page's revisions from the API
	api_session = Session("https://en.wikipedia.org/w/api.php")
	revs = api_session.revisions.query(
		titles={"User:EpochFail"}, 
		properties={'ids', 'sha1'},
		direction="newer"
	)
	
	# Creates a revsion event iterator
	rev_events = ((rev['sha1'], rev) for rev in revs)
	
	# Detect and print reverts
	for revert in reverts.detect(rev_events):
		print("{0} reverted back to {1}".format(revert.reverting['revid'],
		                                        revert.reverted_to['revid']))

For more examples, see scripts inside ``examples/``.

Core modules
============
``api``
	A set of utilities for interacting with MediaWiki's web API.
	
	* Session(...) -- Constructs an API session with a MediaWiki installation.  Contains convenience methods for accessing ``prop=revisions``,  ``list=usercontribs``, ``meta=siteinfo``, and ``list=recentchanges``.

``database``
	A set of utilities for interacting with MediaWiki's database.
	
	* DB(...) -- Constructs a mysql database connector with convenience methods	for accessing ``revision``, ``archive``, ``page``, ``user``, and ``recentchanges``.

``types``
	A set of types for working with MediaWiki data.
	
	* Timestamp(...) -- Constructs a robust datatype for dealing with MediaWikis common timestamp formats

``xml_dump``
	A set of utilities for iteratively processing with MediaWiki's XML database dumps.
	
	* Iterator(..) -- Constructs an iterator over a standard XML dump.  Dumps contain site_info and pages.  Pages contain metadata and revisions.  Revisions contain metadata and text.  This is probably why you are here.
	* map(..) -- Applies a function to a set of dump files (``Iterators``) using the multiprocessing module and aggregates the output.

Libraries
=========
``lib.persistence``
	A set of utilities for tracking the persistence of content between revisions
	
	* State(...) -- Constructs an object that represents the current content persistence state of a page.  Reports useful details about content when updated.

``lib.reverts``
	A set of utilities for performing revert detection
	
	* Detector(...) -- Constructs an identity revert detector that can be updated manually over the history of a page. 
	* detect(...) -- Detects reverts in a sequence of revision events.

``lib.sessions``
	A set of utilities for grouping revisions and other events into sessions
	
	* Cache(...) -- Constructs a cache of recent user actions that can be updated manually in order to detect sessions.
	* cluster(...) -- Clusters a sequence of user actions into sessions.

``lib.titles``
	A set of utilities for normalizing and parsing page titles
	
	* Parser(...) -- Constructs a parser with a set of namespaces that can be used to parse and normalize page titles. 
	* normalize(...) -- Normalizes a page title.  



About the author
================
Aaron Halfaker (aaron.halfaker@gmail.com) -- http://halfaker.info -- http://en.wikipedia.org/User:EpochFail


Contributors
============
None yet.  See http://bitbucket.org/halfak/mediawiki-utilities
