"""
A package with utilities for managing the persistent word analysis across text
versions of a document.  `PersistenceState` is the highest level of the
interface and the part of the system that's most interesting externally.  `Word`s
are also very important.  The current implementation of `Word` only accounts for
how the number of revisions in which a Word is visible.  If persistent word
views (or something similar) is intended to be kept, refactoring will be
necessary.
"""

from .state import State
from .tokens import Tokens, Token
from . import defaults
