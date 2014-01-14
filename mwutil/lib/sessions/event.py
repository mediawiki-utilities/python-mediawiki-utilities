import logging
from collections import namedtuple

from ...types import Timestamp

logger = logging.getLogger("mw.lib.sessions.event")

Event = namedtuple("Event", ['user', 'timestamp', 'data'])
