from itertools import chain

from ...types import Timestamp
from ...util import none_or
from . import defaults
from .functions import detect


def check_rev(session, rev, **kwargs):
    """
    Checks whether a revision (database row) was reverted (identity) and returns
    a named tuple of Revert(reverting, reverteds, reverted_to).

    :Parameters:
        session : :class:`mw.api.Session`
            An API session to make use of
        rev : dict
            a revision dict containing 'revid' and 'page.id'
        radius : int
            the maximum number of revisions that can be reverted
        before : :class:`mw.Timestamp`
            if set, limits the search for *reverting* revisions to those which were saved before this timestamp
        properties : set( str )
            a set of properties to include in revisions (see :class:`mw.api.Revisions`)
    """

    # extract rev_id, sha1, page_id
    if 'revid' in rev:
        rev_id = rev['revid']
    else:
        raise TypeError("rev must have 'rev_id'")
    if 'page' in rev:
        page_id = rev['page']['id']
    elif 'pageid' in rev:
        page_id = rev['pageid']
    else:
        raise TypeError("rev must have 'page' or 'pageid'")

    # run the regular check
    return check(session, rev_id, page_id=page_id, **kwargs)


def check(session, rev_id, page_id=None, radius=defaults.RADIUS,
          before=None, properties=None):
    """
    Checks whether a revision was reverted (identity) and returns a named tuple
    of Revert(reverting, reverteds, reverted_to).

    :Parameters:
        session : :class:`mw.api.Session`
            An API session to make use of
        rev_id : int
            the ID of the revision to check
        page_id : int
            the ID of the page the revision occupies (slower if not provided)
        radius : int
            the maximum number of revisions that can be reverted
        before : :class:`mw.Timestamp`
            if set, limits the search for *reverting* revisions to those which were saved before this timestamp
        properties : set( str )
            a set of properties to include in revisions (see :class:`mw.api.Revisions`)
    """

    if not hasattr(session, "revisions"):
        raise TypeError("session wrong type.  Expected a mw.api.Session.")

    rev_id = int(rev_id)
    radius = int(radius)
    page_id = none_or(page_id, int)
    before = none_or(before, Timestamp)
    properties = set(properties) if properties is not None else set()

    # If we don't have the page_id, we're going to need to look them up
    if page_id is None:
        rev = session.revisions.get(rev_id)
        page_id = row['page']['id']

    # Load history and current rev
    current_and_past_revs = list(session.revisions.query(
        pageids={page_id},
        limit=radius + 1,
        start_id=rev_id + 1,  # Ensures that we capture the current revision
        direction="older",
        properties={'ids', 'timestamp', 'sha1'} | properties
    ))

    try:
        # Extract current rev and reorder history
        current_rev, past_revs = (
            current_and_past_revs[0],  # Current rev is the first one returned
            reversed(current_and_past_revs[1:])  # The rest are past revs, but they are in the wrong order
        )
    except IndexError:
        # Only way to get here is if there isn't enough history.  Couldn't be
        # reverted.  Just return None.
        return None

    # Load future revisions
    future_revs = session.revisions.query(
        pageids={page_id},
        limit=radius,
        start_id=rev_id,
        end=before,
        direction="newer",
        properties={'ids', 'timestamp', 'sha1'} | properties
    )

    # Convert to an iterable of (checksum, rev) pairs for detect() to consume
    checksum_revisions = chain(
        ((rev['sha1'], rev) for rev in past_revs),
        [(current_rev['sha1'], current_rev)],
        ((rev['sha1'], rev) for rev in future_revs)
    )

    for revert in detect(checksum_revisions, radius=radius):
        # Check that this is a relevant revert
        if rev_id in [rev['revid'] for rev in revert.reverteds]:
            return revert

    return None
