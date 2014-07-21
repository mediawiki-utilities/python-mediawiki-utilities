from .detector import Detector
from . import defaults


def detect(checksum_revisions, radius=defaults.RADIUS):
    """
    Detects reverts that occur in a sequence of revisions.  Note that,
    `revision` data meta will simply be returned in the case of a revert.

    This function serves as a convenience wrapper around calls to
    :class:`Detector`'s :meth:`~Detector.process`
    method.

    :Parameters:
        checksum_revisions : iter( ( checksum : str, revision : `mixed` ) )
            an iterable over tuples of checksum and revision meta data
        radius : int
            the maximum revision distance that a revert can span.

    :Return:
        a iterator over :class:`Revert`

    :Example:
        >>> from mw.lib import reverts
        >>>
        >>> checksum_revisions = [
        ...     ("aaa", {'rev_id': 1}),
        ...     ("bbb", {'rev_id': 2}),
        ...     ("aaa", {'rev_id': 3}),
        ...     ("ccc", {'rev_id': 4})
        ... ]
        >>>
        >>> list(reverts.detect(checksum_revisions))
        [Revert(reverting={'rev_id': 3}, reverteds=[{'rev_id': 2}], reverted_to={'rev_id': 1})]

    """

    revert_detector = Detector(radius)

    for checksum, revision in checksum_revisions:
        revert = revert_detector.process(checksum, revision)
        if revert is not None:
            yield revert

# For backwards compatibility
reverts = detect
