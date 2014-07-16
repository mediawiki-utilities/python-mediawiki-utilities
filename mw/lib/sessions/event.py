import logging
from collections import namedtuple

logger = logging.getLogger("mw.lib.sessions.event")


# class Event:
#   __slots__ = ('user', 'timestamp', 'data')
#
#   def __init__(self, user, timestamp, data=None):
#       self.user = user
#       self.timestamp = Timestamp(timestamp)
#       self.data = data

Event = namedtuple("Event", ['user', 'timestamp', 'data'])


def unpack_events(events):
    return list(e.data for e in events)
