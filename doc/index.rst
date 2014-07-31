.. mediawiki-utilities documentation master file, created by
   sphinx-quickstart on Thu Apr 10 17:31:47 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===================
MediaWiki Utilities
===================

MediaWiki Utilities is an open source (MIT Licensed) library developed by Aaron Halfaker for extracting and processing data from MediaWiki installations, slave databases and xml dumps.

**Instal with pip:** ``pip install mediawiki-utilities``

**Note:** *Use of this library requires Python 3 or later.*

Types
=====
:ref:`mw.Timestamp <mw.types>`
	A simple datatype for handling MediaWiki's various time formats.

Core modules
============

:ref:`mw.api <mw.api>`
	A set of utilities for interacting with MediaWiki's web API.
	
	* :class:`~mw.api.Session` -- Constructs an API session with a MediaWiki installation.  Contains convenience methods for accessing ``prop=revisions``,  ``list=usercontribs``, ``meta=siteinfo``, ``list=deletedrevs`` and ``list=recentchanges``.

:ref:`mw.database <mw.database>`
	A set of utilities for interacting with MediaWiki's database.
	
	* :class:`~mw.database.DB` -- Constructs a mysql database connector with convenience methods for accessing ``revision``, ``archive``, ``page``, ``user``, and ``recentchanges``.

:ref:`mw.xml_dump <mw.xml_dump>`
	A set of utilities for processing MediaWiki's XML database dumps quickly and without dealing with streaming XML. 
	
	* :func:`~mw.xml_dump.map` -- Applies a function to a set of dump files (:class:`~mw.xml_dump.Iterator`) using :class:`multiprocessing` and aggregates the output.
	* :class:`~mw.xml_dump.Iterator` -- Constructs an iterator over a standard XML dump.  Dumps contain site_info and pages.  Pages contain metadata and revisions.  Revisions contain metadata and text.  This is probably why you are here.

Libraries
=========

:ref:`mw.lib.persistence <mw.lib.persistence>`
	A set of utilities for tracking the persistence of content between revisions.
	
	* :class:`~mw.lib.persistence.State` -- Constructs an object that represents the current content persistence state of a page.  Reports useful details about the persistence of content when updated.

:ref:`mw.lib.reverts <mw.lib.reverts>`
	A set of utilities for performing revert detection
	
	* :func:`~mw.lib.reverts.detect` -- Detects reverts in a sequence of revision events.
	* :class:`~mw.lib.reverts.Detector` -- Constructs an identity revert detector that can be updated manually over the history of a page. 

:ref:`mw.lib.sessions <mw.lib.sessions>`
	A set of utilities for grouping revisions and other events into sessions
	
	* :func:`~mw.lib.sessions.cluster` -- Clusters a sequence of user actions into sessions.
	* :class:`~mw.lib.sessions.Cache` -- Constructs a cache of recent user actions that can be updated manually in order to detect sessions.

:ref:`mw.lib.title <mw.lib.title>`
	A set of utilities for normalizing and parsing page titles
	
	* :func:`~mw.lib.title.normalize` -- Normalizes a page title.  
	* :class:`~mw.lib.title.Parser` -- Constructs a parser with a set of namespaces that can be used to parse and normalize page titles. 

About the author
================
:name: 
	Aaron Halfaker
:email:
	aaron.halfaker@gmail.com
:website:
	http://halfaker.info --
	http://en.wikipedia.org/wiki/User:EpochFail


Contributors
============
None yet.  See http://github.com/halfak/mediawiki-utilities.  Pull requests are encouraged.


Indices and tables
==================

.. toctree::
   :maxdepth: 2
   
   types
   core/api
   core/database
   core/xml_dump
   lib/persistence
   lib/reverts
   lib/sessions
   lib/title

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

