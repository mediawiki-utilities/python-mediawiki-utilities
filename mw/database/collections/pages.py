import logging

from .collection import Collection
from ...util import none_or

logger = logging.getLogger("mw.database.collections.pages")


class Pages(Collection):
    def get(self, page_id=None, namespace_title=None, rev_id=None):
        """
        Gets a single page based on a legitimate identifier of the page.  Note
        that namespace_title expects a tuple of namespace ID and title.

        :Parameters:
            page_id : int
                Page ID
            namespace_title : ( int, str )
                the page's namespace ID and title
            rev_id : int
                a revision ID included in the page's history

        :Returns:
            iterator over result rows
        """

        page_id = none_or(page_id, int)
        namespace_title = none_or(namespace_title, tuple)
        rev_id = none_or(rev_id, int)

        query = """
        SELECT page.*
        FROM page
        """
        values = []

        if page_id is not None:
            query += """
                WHERE page_id = ?
            """
            values.append(page_id)

        if namespace_title is not None:
            namespace, title = namespace_title

            query += " WHERE page_namespace = ? and page_title = ? "
            values.extend([int(namespace), str(title)])

        elif rev_id is not None:
            query += """
                WHERE page_id = (SELECT rev_page FROM revision WHERE rev_id = ?)
            """
            values.append(rev_id)

        else:
            raise TypeError("Must specify a page identifier.")

        cursor = self.db.shared_connection.cursor()
        cursor.execute(
            query,
            values
        )

        for row in cursor:
            return row
