.. _mw.api:

============================================================
mw.api -- utilities for extracting data from MediaWiki API's
============================================================

Session
=======

.. autoclass:: mw.api.Session
   :members:
   :member-order: bysource


Collections
===========

.. autoclass:: mw.api.DeletedRevs
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