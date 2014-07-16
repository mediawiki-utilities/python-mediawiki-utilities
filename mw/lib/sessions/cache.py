import logging
from collections import namedtuple

from ...util import Heap
from ...types import Timestamp
from . import defaults
from .event import Event, unpack_events


logger = logging.getLogger("mw.lib.sessions.cache")

Session = namedtuple("Session", ["user", "events"])
"""
Represents a user session (a cluster over events for a user).  This class
behaves like :class:`collections.namedtuple`.  Note that the datatypes of
`events`, is not specified since those types will depend on the revision data
provided during revert detection.

:Members:
    **user**
        A hashable user identifier : `hashable`
    **events**
        A list of event data : list( `mixed` )
"""


class Cache:
    """
    A cache of recent user session.  Since sessions expire once activities stop
    for at least `cutoff` seconds, this class manages a cache of *active*
    sessions.

    :Parameters:
        cutoff : int
            Maximum amount of time in seconds between session events

    :Example:
        >>> from mw.lib import sessions
        >>>
        >>> cache = sessions.Cache(cutoff=3600)
        >>>
        >>> list(cache.process("Willy on wheels", 100000, {'rev_id': 1}))
        []
        >>> list(cache.process("Walter", 100001, {'rev_id': 2}))
        []
        >>> list(cache.process("Willy on wheels", 100001, {'rev_id': 3}))
        []
        >>> list(cache.process("Walter", 100035, {'rev_id': 4}))
        []
        >>> list(cache.process("Willy on wheels", 103602, {'rev_id': 5}))
        [Session(user='Willy on wheels', events=[{'rev_id': 1}, {'rev_id': 3}])]
        >>> list(cache.get_active_sessions())
        [Session(user='Walter', events=[{'rev_id': 2}, {'rev_id': 4}]), Session(user='Willy on wheels', events=[{'rev_id': 5}])]


    """

    def __init__(self, cutoff=defaults.CUTOFF):
        self.cutoff = int(cutoff)

        self.recently_active = Heap()
        self.active_users = {}

    def process(self, user, timestamp, data=None):
        """
        Processes a user event.

        :Parameters:
            user : `hashable`
                A hashable value to identify a user (`int` or `str` are OK)
            timestamp : :class:`mw.Timestamp`
                The timestamp of the event
            data : `mixed`
                Event meta data

        :Returns:
            A generator of :class:`~mw.lib.sessions.Session` expired after
            processing the user event.
        """
        event = Event(user, Timestamp(timestamp), data)

        for user, events in self._clear_expired(event.timestamp):
            yield Session(user, unpack_events(events))

        # Apply revision
        if event.user in self.active_users:
            events = self.active_users[event.user]
        else:
            events = []
            self.active_users[event.user] = events
            self.recently_active.push((event.timestamp, events))

        events.append(event)

    def get_active_sessions(self):
        """
        Retrieves the active, unexpired sessions.

        :Returns:
            A generator of :class:`~mw.lib.sessions.Session`

        """
        for last_timestamp, events in self.recently_active:
            yield Session(events[-1].user, unpack_events(events))

    def _clear_expired(self, timestamp):

        # Cull old sessions
        while (len(self.recently_active) > 0 and
               timestamp - self.recently_active.peek()[0] >= self.cutoff):

            _, events = self.recently_active.pop()

            if timestamp - events[-1].timestamp >= self.cutoff:
                del self.active_users[events[-1].user]
                yield events[-1].user, events
            else:
                self.recently_active.push((events[-1].timestamp, events))

    def __repr__(self):
        return "%s(%s)".format(self.__class__.__name__, repr(self.cutoff))
