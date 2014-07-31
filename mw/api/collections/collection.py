import re


class Collection:
    """
    Represents a collection of items that can be queried via the API.  This is
    an abstract base class that should be extended
    """

    TIMESTAMP = re.compile(r"[0-9]{4}-?[0-9]{2}-?[0-9]{2}T?" +
                           r"[0-9]{2}:?[0-9]{2}:?[0-9]{2}Z?")
    """
    A regular expression for matching the API's timestamp format.
    """

    DIRECTIONS = {'newer', 'older'}
    """
    A set of potential direction names.
    """

    def __init__(self, session):
        """
        :Parameters:
            session : `mw.api.Session`
                An api session to use for post & get.
        """
        self.session = session

    def _check_direction(self, direction):
        if direction is None:
            return direction
        else:
            direction = str(direction)

            assert direction in {None} | self.DIRECTIONS, \
                "Direction must be one of {0}".format(self.DIRECTIONS)

            return direction

    def _check_timestamp(self, timestamp):
        if timestamp is None:
            return timestamp
        else:
            timestamp = str(timestamp)

            if not self.TIMESTAMP.match(timestamp):
                raise TypeError(
                    "{0} is not formatted like ".format(repr(timestamp)) +
                    "a MediaWiki timestamp."
                )

            return timestamp

    def _items(self, items, none=True, levels=None, type=lambda val: val):

        if none and items is None:
            return None
        else:
            items = {str(type(item)) for item in items}

            if levels is not None:
                levels = {str(level) for level in levels}

                assert len(items - levels) == 0, \
                    "items {0} not in levels {1}".format(
                        items - levels, levels)

            return "|".join(items)
