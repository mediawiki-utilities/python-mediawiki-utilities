"""
This module provides a set of utilities for detecting identity reverts in
revisioned content.

To detect reverts in a stream of revisions to a single page, you can use
:func:`detect`.  If you'll be detecting reverts in a collection of pages or
would, for some other reason, prefer to process revisions one at a time,
:class:`Detector` and it's :meth:`~Detector.process` will allow you to do so.

To detect reverts one-at-time and arbitrarily, you can user the `check()`
functions:

* :func:`database.check` and :func:`database.check_row` use a :class:`mw.database.DB`
* :func:`api.check` and :func:`api.check_rev` use a :class:`mw.api.Session`

Note that these functions are less performant than detecting reverts in a
stream of page revisions.  This can be practical when trying to identify
reverted revisions in a user's contribution history.
"""
from .detector import Detector, Revert
from .functions import detect, reverts
from . import database
from . import api
from . import defaults
