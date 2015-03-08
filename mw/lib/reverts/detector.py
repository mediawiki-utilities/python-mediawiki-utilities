from collections import namedtuple

from ...util import ordered
from . import defaults

Revert = namedtuple("Revert", ['reverting', 'reverteds', 'reverted_to'])
"""
Represents a revert event.  This class behaves like
:class:`collections.namedtuple`.  Note that the datatypes of `reverting`,
`reverteds` and `reverted_to` is not specified since those types will depend
on the revision data provided during revert detection.

:Members:
    **reverting**
        The reverting revision data : `mixed`
    **reverteds**
        The reverted revision data (ordered chronologically) : list( `mixed` )
    **reverted_to**
        The reverted-to revision data : `mixed`
"""


class Detector(ordered.HistoricalMap):
    """
    Detects revert events in a stream of revisions (to the same page) based on
    matching checksums.  To detect reverts, construct an instance of this class and call
    :meth:`process` in chronological order (``direction == "newer"``).

    See `<https://meta.wikimedia.org/wiki/R:Identity_revert>`_

    :Parameters:
        radius : int
            a positive integer indicating the maximum revision distance that a revert can span.

    :Example:
        >>> from mw.lib import reverts
        >>> detector = reverts.Detector()
        >>>
        >>> detector.process("aaa", {'rev_id': 1})
        >>> detector.process("bbb", {'rev_id': 2})
        >>> detector.process("aaa", {'rev_id': 3})
        Revert(reverting={'rev_id': 3}, reverteds=[{'rev_id': 2}], reverted_to={'rev_id': 1})
        >>> detector.process("ccc", {'rev_id': 4})

    """

    def __init__(self, radius=defaults.RADIUS):
        """
        :Parameters:
            radius : int
                a positive integer indicating the maximum revision distance that a revert can span.
        """
        if radius < 1:
            raise TypeError("invalid radius. Expected a positive integer.")
        super().__init__(maxlen=radius + 1)

    def process(self, checksum, revision=None):
        """
        Process a new revision and detect a revert if it occurred.  Note that
        you can pass whatever you like as `revision` and it will be returned in
        the case that a revert occurs.

        :Parameters:
            checksum : str
                Any identity-machable string-based hash of revision content
            revision : `mixed`
                Revision meta data.  Note that any data will just be returned in the
                case of a revert.

        :Returns:
            a :class:`~mw.lib.reverts.Revert` if one occured or `None`
        """
        revert = None

        if checksum in self:  # potential revert

            reverteds = list(self.up_to(checksum))

            if len(reverteds) > 0:  # If no reverted revisions, this is a noop
                revert = Revert(revision, reverteds, self[checksum])

        self.insert(checksum, revision)
        return revert
