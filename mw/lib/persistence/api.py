from .. import reverts
from ...util import none_or
from .state import State


def track(session, rev_id, page_id=None, revert_radius=reverts.defaults.RADIUS,
          future_revisions=reverts.defaults.RADIUS, properties=None):
    """
    Computes a persistence score for a revision by processing the revisions
    that took place around it.

    :Parameters:
        session : :class:`mw.api.Session`
            An API session to make use of
        rev_id : int
            the ID of the revision to check
        page_id : int
            the ID of the page the revision occupies (slower if not provided)
        revert_radius : int
            a positive integer indicating the maximum number of revisions that can be reverted
    """

    if not hasattr(session, "revisions"):
        raise TypeError("session is wrong type.  Expected a mw.api.Session.")

    rev_id = int(rev_id)
    page_id = none_or(page_id, int)
    revert_radius = int(revert_radius)
    if revert_radius < 1:
        raise TypeError("invalid radius.  Expected a positive integer.")
    properties = set(properties) if properties is not None else set()


    # If we don't have the page_id, we're going to need to look them up
    if page_id is None:
        rev = session.revisions.get(rev_id, properties={'ids'})
        page_id = rev['page']['pageid']

    # Load history and current rev
    current_and_past_revs = list(session.revisions.query(
        pageids={page_id},
        limit=revert_radius + 1,
        start_id=rev_id,
        direction="older",
        properties={'ids', 'timestamp', 'content', 'sha1'} | properties
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
        limit=future_revisions,
        start_id=rev_id + 1, # Ensures that we skip the current revision
        direction="newer",
        properties={'ids', 'timestamp', 'content', 'sha1'} | properties
    )

    state = State(revert_radius=revert_radius)

    # Process old revisions
    for rev in past_revs:
        state.process(rev.get('*', ""), rev, rev.get('sha1'))

    # Process current revision
    _, tokens_added, _ = state.process(current_rev.get('*'), current_rev,
                                         current_rev.get('sha1'))

    # Process new revisions
    future_revs = list(future_revs)
    for rev in future_revs:
        state.process(rev.get('*', ""), rev, rev.get('sha1'))

    return current_rev, tokens_added, future_revs

score = track
