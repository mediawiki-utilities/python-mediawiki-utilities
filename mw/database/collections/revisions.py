import logging
import time
from itertools import chain

from ...types import Timestamp
from ...util import iteration, none_or
from .collection import Collection

logger = logging.getLogger("mw.database.collections.revisions")


class AllRevisions(Collection):
    def get(self, rev_id, include_page=False):
        """
        Gets a single revisions by ID.  Checks both the ``revision`` and
        ``archive`` tables.  This method throws a :class:`KeyError` if a
        revision cannot be found.

        :Parameters:
            rev_id : int
                Revision ID
            include_page : bool
                Join revision returned against ``page``

        :Returns:
            A revision row
        """
        rev_id = int(rev_id)
        try:
            rev_row = self.db.revisions.get(rev_id, include_page=include_page)
        except KeyError as e:
            rev_row = self.db.archives.get(rev_id)

        return rev_row

    def query(self, *args, **kwargs):
        """
        Queries revisions (excludes revisions to deleted pages)

        :Parameters:
            page_id : int
                Page identifier.  Filter revisions to this page.
            user_id : int
                User identifier.  Filter revisions to those made by this user.
            user_text : str
                User text (user_name or IP address).  Filter revisions to those
                made by this user.
            before : :class:`mw.Timestamp`
                Filter revisions to those made before this timestamp.
            after : :class:`mw.Timestamp`
                Filter revisions to those made after this timestamp.
            before_id : int
                Filter revisions to those with an ID before this ID
            after_id : int
                Filter revisions to those with an ID after this ID
            direction : str
                "newer" or "older"
            limit : int
                Limit the number of results
            include_page : bool
                Join revisions returned against ``page``

        :Returns:
            An iterator over revision rows.
        """

        revisions = self.db.revisions.query(*args, **kwargs)
        archives = self.db.archives.query(*args, **kwargs)

        if 'direction' in kwargs:
            direction = kwargs['direction']
            if direction not in self.DIRECTIONS:
                raise TypeError("direction must be in {0}".format(self.DIRECTIONS))

            if direction == "newer":
                collated_revisions = iteration.sequence(
                    revisions,
                    archives,
                    compare=lambda r1, r2: \
                            (r1['rev_timestamp'], r1['rev_id']) <=
                            (r2['rev_timestamp'], r2['rev_id'])
                )
            else:  # direction == "older"
                collated_revisions = iteration.sequence(
                    revisions,
                    archives,
                    compare=lambda r1, r2: \
                            (r1['rev_timestamp'], r1['rev_id']) >=
                            (r2['rev_timestamp'], r2['rev_id'])
                )
        else:
            collated_revisions = chain(revisions, archives)

        if 'limit' in kwargs:
            limit = kwargs['limit']

            for i, rev in enumerate(collated_revisions):
                yield rev
                if i >= limit:
                    break

        else:
            for rev in collated_revisions:
                yield rev


class Revisions(Collection):
    
    def get(self, rev_id, include_page=False):
        """
        Gets a single revisions by ID.  Checks the ``revision`` table.   This
        method throws a :class:`KeyError` if a revision cannot be found.

        :Parameters:
            rev_id : int
                Revision ID
            include_page : bool
                Join revision returned against ``page``

        :Returns:
            A revision row
        """
        rev_id = int(rev_id)

        query = """
            SELECT *, FALSE AS archived FROM revision
        """
        if include_page:
            query += """
                INNER JOIN page ON page_id = rev_page
            """

        query += " WHERE rev_id = ?"

        cursor.execute(query, [rev_id])

        for row in cursor:
            return row

        raise KeyError(rev_id)

    def query(self, page_id=None, user_id=None, user_text=None,
              before=None, after=None, before_id=None, after_id=None,
              direction=None, limit=None, include_page=False):
        """
        Queries revisions (excludes revisions to deleted pages)

        :Parameters:
            page_id : int
                Page identifier.  Filter revisions to this page.
            user_id : int
                User identifier.  Filter revisions to those made by this user.
            user_text : str
                User text (user_name or IP address).  Filter revisions to those
                made by this user.
            before : :class:`mw.Timestamp`
                Filter revisions to those made before this timestamp.
            after : :class:`mw.Timestamp`
                Filter revisions to those made after this timestamp.
            before_id : int
                Filter revisions to those with an ID before this ID
            after_id : int
                Filter revisions to those with an ID after this ID
            direction : str
                "newer" or "older"
            limit : int
                Limit the number of results
            include_page : bool
                Join revisions returned against ``page``

        :Returns:
            An iterator over revision rows.
        """
        start_time = time.time()

        page_id = none_or(page_id, int)
        user_id = none_or(user_id, int)
        user_text = none_or(user_text, str)
        before = none_or(before, Timestamp)
        after = none_or(after, Timestamp)
        before_id = none_or(before_id, int)
        after_id = none_or(after_id, int)
        direction = none_or(direction, levels=self.DIRECTIONS)
        include_page = bool(include_page)

        query = """
            SELECT *, FALSE AS archived FROM revision
        """

        if include_page:
            query += """
                INNER JOIN page ON page_id = rev_page
            """

        query += """
            WHERE 1
        """
        values = []

        if page_id is not None:
            query += " AND rev_page = ? "
            values.append(page_id)
        if user_id is not None:
            query += " AND rev_user = ? "
            values.append(user_id)
        if user_text is not None:
            query += " AND rev_user_text = ? "
            values.append(user_text)
        if before is not None:
            query += " AND rev_timestamp < ? "
            values.append(before.short_format())
        if after is not None:
            query += " AND rev_timestamp > ? "
            values.append(after.short_format())
        if before_id is not None:
            query += " AND rev_id < ? "
            values.append(before_id)
        if after_id is not None:
            query += " AND rev_id > ? "
            values.append(after_id)

        if direction is not None:
            
            direction = ("ASC " if direction == "newer" else "DESC ")
            
            if before_id != None or after_id != None:
                query += " ORDER BY rev_id {0}, rev_timestamp {0}".format(direction)
            else:
                query += " ORDER BY rev_timestamp {0}, rev_id {0}".format(direction)

        if limit is not None:
            query += " LIMIT ? "
            values.append(limit)

        cursor = self.db.shared_connection.cursor()
        cursor.execute(query, values)
        count = 0
        for row in cursor:
            yield row
            count += 1

        logger.debug("%s revisions read in %s seconds" % (count, time.time() - start_time))


class Archives(Collection):
    def get(self, rev_id):
        """
        Gets a single revisions by ID.  Checks the ``archive`` table. This
        method throws a :class:`KeyError` if a revision cannot be found.

        :Parameters:
            rev_id : int
                Revision ID

        :Returns:
            A revision row
        """
        rev_id = int(rev_id)

        query = """
            SELECT
                ar_id,
                ar_rev_id AS rev_id,
                ar_page_id AS rev_page,
                ar_page_id AS page_id,
                ar_title AS page_title,
                ar_namespace AS page_namespace,
                ar_text_id AS rev_text_id,
                ar_comment AS rev_comment,
                ar_user AS rev_user,
                ar_user_text AS rev_user_text,
                ar_timestamp AS rev_timestamp,
                ar_minor_edit AS rev_minor_edit,
                ar_deleted AS rev_deleted,
                ar_len AS rev_len,
                ar_parent_id AS rev_parent_id,
                ar_sha1 AS rev_sha1,
                TRUE AS archived
            FROM archive
            WHERE ar_rev_id = ?
        """

        cursor.execute(query, [rev_id])
        for row in cursor:
            return row

        raise KeyError(rev_id)

    def query(self, page_id=None, user_id=None, user_text=None,
              before=None, after=None, before_id=None, after_id=None,
              before_ar_id=None, after_ar_id=None,
              direction=None, limit=None, include_page=True):
        """
        Queries archived revisions (revisions of deleted pages)

        :Parameters:
            page_id : int
                Page identifier.  Filter revisions to this page.
            user_id : int
                User identifier.  Filter revisions to those made by this user.
            user_text : str
                User text (user_name or IP address).  Filter revisions to those
                made by this user.
            before : :class:`mw.Timestamp`
                Filter revisions to those made before this timestamp.
            after : :class:`mw.Timestamp`
                Filter revisions to those made after this timestamp.
            before_id : int
                Filter revisions to those with an ID before this ID
            after_id : int
                Filter revisions to those with an ID after this ID
            direction : str
                "newer" or "older"
            limit : int
                Limit the number of results
            include_page : bool
                This field is ignored.  It's only here for compatibility with
                :class:`mw.database.Revision`.

        :Returns:
            An iterator over revision rows.
        """
        page_id = none_or(page_id, int)
        user_id = none_or(user_id, int)
        before = none_or(before, Timestamp)
        after = none_or(after, Timestamp)
        before_id = none_or(before_id, int)
        after_id = none_or(after_id, int)
        direction = none_or(direction, levels=self.DIRECTIONS)
        limit = none_or(limit, int)

        start_time = time.time()
        cursor = self.db.shared_connection.cursor()

        query = """
            SELECT
                ar_id,
                ar_rev_id AS rev_id,
                ar_page_id AS rev_page,
                ar_page_id AS page_id,
                ar_title AS page_title,
                ar_namespace AS page_namespace,
                ar_text_id AS rev_text_id,
                ar_comment AS rev_comment,
                ar_user AS rev_user,
                ar_user_text AS rev_user_text,
                ar_timestamp AS rev_timestamp,
                ar_minor_edit AS rev_minor_edit,
                ar_deleted AS rev_deleted,
                ar_len AS rev_len,
                ar_parent_id AS rev_parent_id,
                ar_sha1 AS rev_sha1,
                TRUE AS archived
            FROM archive
        """

        query += """
            WHERE 1
        """
        values = []

        if page_id is not None:
            query += " AND ar_page_id = ? "
            values.append(page_id)
        if user_id is not None:
            query += " AND ar_user = ? "
            values.append(user_id)
        if user_text is not None:
            query += " AND ar_user_text = ? "
            values.append(user_text)
        if before is not None:
            query += " AND ar_timestamp < ? "
            values.append(before.short_format())
        if after is not None:
            query += " AND ar_timestamp > ? "
            values.append(after.short_format())
        if before_id is not None:
            query += " AND ar_rev_id < ? "
            values.append(before_id)
        if after_id is not None:
            query += " AND ar_rev_id > ? "
            values.append(after_id)
        if before_ar_id is not None:
            query += " AND ar_id < ? "
            values.append(before_ar_id)
        if after_ar_id is not None:
            query += " AND ar_id > ? "
            values.append(after_ar_id)

        if direction is not None:
            dir = ("ASC " if direction == "newer" else "DESC ")
            
            if before is not None or after is not None:
                query += " ORDER BY ar_timestamp {0}, ar_rev_id {0}".format(dir)
            elif before_id is not None or after_id is not None:
                query += " ORDER BY ar_rev_id {0}, ar_timestamp {0}".format(dir)
            else:
                query += " ORDER BY ar_id {0}".format(dir)
        
        if limit is not None:
            query += " LIMIT ? "
            values.append(limit)

        cursor.execute(query, values)
        count = 0
        for row in cursor:
            yield row
            count += 1

        logger.debug("%s revisions read in %s seconds" % (count, time.time() - start_time))
