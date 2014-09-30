import logging
import time

from ...types import Timestamp
from ...util import none_or
from .collection import Collection

logger = logging.getLogger("mw.database.collections.pages")


class RecentChanges(Collection):
    # (https://www.mediawiki.org/wiki/Manual:Recentchanges_table)
    TYPES = {
        'edit': 0,  # edit of existing page
        'new': 1,  # new page
        'move': 2,  # Marked as obsolete
        'log': 3,  # log action (introduced in MediaWiki 1.2)
        'move_over_redirect': 4,  # Marked as obsolete
        'external': 5  # An external recent change. Primarily used by Wikidata
    }

    def listen(self, last=None, types=None, max_wait=5):
        """
        Listens to the recent changes table.  Given no parameters, this function
        will return an iterator over the entire recentchanges table and then
        continue to "listen" for new changes to come in every 5 seconds.

        :Parameters:
            last : dict
                a recentchanges row to pick up after
            types : set ( str )
                a set of recentchanges types to filter for
            max_wait : float
                the maximum number of seconds to wait between repeated queries

        :Returns:
            A never-ending iterator over change rows.
        """
        while True:
            if last is not None:
                after = last['rc_timestamp']
                after_id = last['rc_id']
            else:
                after = None
                after_id = None

            start = time.time()
            rcs = self.query(after=after, after_id=after_id, direction="newer")

            count = 0
            for rc in rcs:
                yield rc
                count += 1

            time.sleep(max_wait - (time.time() - start))

    def query(self, before=None, after=None, before_id=None, after_id=None,
              types=None, direction=None, limit=None):
        """
        Queries the ``recentchanges`` table.  See
        `<https://www.mediawiki.org/wiki/Manual:Recentchanges_table>`_

        :Parameters:
            before : :class:`mw.Timestamp`
                The maximum timestamp
            after : :class:`mw.Timestamp`
                The minimum timestamp
            before_id : int
                The minimum ``rc_id``
            after_id : int
                The maximum ``rc_id``
            types : set ( str )
                Which types of changes to return?

                * ``edit`` -- Edits to existing pages
                * ``new`` -- Edits that create new pages
                * ``move`` -- (obsolete)
                * ``log`` -- Log actions (introduced in MediaWiki 1.2)
                * ``move_over_redirect`` -- (obsolete)
                * ``external`` -- An external recent change. Primarily used by Wikidata

            direction : str
                "older" or "newer"
            limit : int
                limit the number of records returned
        """
        before = none_or(before, Timestamp)
        after = none_or(after, Timestamp)
        before_id = none_or(before_id, int)
        after_id = none_or(after_id, int)
        types = none_or(types, levels=self.TYPES)
        direction = none_or(direction, levels=self.DIRECTIONS)
        limit = none_or(limit, int)

        query = """
            SELECT * FROM recentchanges
            WHERE 1
        """
        values = []

        if before is not None:
            query += " AND rc_timestamp < %s "
            values.append(before.short_format())
        if after is not None:
            query += " AND rc_timestamp < %s "
            values.append(after.short_format())
        if before_id is not None:
            query += " AND rc_id < %s "
            values.append(before_id)
        if after_id is not None:
            query += " AND rc_id < %s "
            values.append(after_id)
        if types is not None:
            query += " AND rc_type IN ({0}) ".format(
                ",".join(self.TYPES[t] for t in types)
            )

        if direction is not None:
            direction = ("ASC " if direction == "newer" else "DESC ")
            query += " ORDER BY rc_timestamp {0}, rc_id {0}".format(dir)

        if limit is not None:
            query += " LIMIT %s "
            values.append(limit)

        cursor.execute(query, values)
        for row in cursor:
            yield row
