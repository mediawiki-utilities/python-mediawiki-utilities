.. _mw.api:

===================================
mw.api -- MediaWiki API abstraction
===================================

This module contains a set of utilities for interacting with the MediaWiki API.

Here's an example of a common usage pattern:
	
	>>> from mw import api
	>>> 
	>>> session = api.Session("https://en.wikipedia.org/w/api.php")
	>>> 
	>>> revisions = session.revisions.query(
	...     properties={'ids', 'content'},
	...     titles={"User:EpochFail"},
	...     direction="newer",
	...     limit=3
	... )
	>>> 
	>>> for rev in revisions:
	...     print(
	...             "rev_id={0}, length={1} characters".format(
	...                     rev['revid'],
	...                     len(rev.get('*', ""))
	...             )
	...     )
	... 
	rev_id=190055192, length=124 characters
	rev_id=276121340, length=132 characters
	rev_id=276121389, length=124 characters

Session
=======

.. autoclass:: mw.api.Session
   :members:
   :member-order: bysource


Collections
===========

.. autoclass:: mw.api.DeletedRevisions
   :members:

.. autoclass:: mw.api.Pages
   :members:

.. autoclass:: mw.api.RecentChanges
   :members:

.. autoclass:: mw.api.Revisions
   :members:

.. autoclass:: mw.api.SiteInfo
   :members:

.. autoclass:: mw.api.UserContribs
   :members:

Errors
======


.. autoclass:: mw.api.errors.APIError
   :members:
   :inherited-members:

.. autoclass:: mw.api.errors.AuthenticationError
   :members:
   :inherited-members:

.. autoclass:: mw.api.errors.MalformedResponse
   :members:
   :inherited-members:
