.. _mw.xml_dump:

==================================
mw.xml_dump -- XML dump processing
==================================

This module is a collection of utilities for efficiently processing MediaWiki's XML database dumps.  There are two important concerns that this module intends to address: *performance* and the *complexity* of streaming XML parsing.

Performance
	Performance is a serious concern when processing large database XML dumps.  Regretfully, the Global Intepreter Lock prevents us from running threads on multiple CPUs.  This library provides a :func:`~mw.xml_dump.map`, a function that maps a dump processsing over a set of dump files using :class:`multiprocessing` to distribute the work over multiple CPUS

Complexity
	Streaming XML parsing is gross.  XML dumps are (1) some site meta data, (2) a collection of pages that contain (3) collections of revisions.  The module allows you to think about dump files in this way and ignore the fact that you're streaming XML.  An :class:`mw.xml_dump.Iterator` contains site meta data and an iterator of :class:`~mw.xml_dump.Page`'s.  A :class:`~mw.xml_dump.Page` contains page meta data and an iterator of :class:`~mw.xml_dump.Revision`'s

The map() function
==================

.. autofunction:: mw.xml_dump.map

Iteration
=========

.. autoclass:: mw.xml_dump.Iterator
   :members:
   :member-order: bysource

.. autoclass:: mw.xml_dump.Page
   :members:
   :member-order: bysource

.. autoclass:: mw.xml_dump.Revision
   :members:
   :member-order: bysource

.. autoclass:: mw.xml_dump.Contributor
   :members:
   :member-order: bysource

Errors
======

.. autoclass:: mw.xml_dump.errors.FileTypeError
   :members:

.. autoclass:: mw.xml_dump.errors.MalformedXML
   :members:
