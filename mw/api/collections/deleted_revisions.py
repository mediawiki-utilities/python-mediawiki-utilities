import logging
import sys

from ...types import Timestamp
from ...util import none_or
from ..errors import MalformedResponse
from .collection import Collection

logger = logging.getLogger("mw.api.collections.deletedrevs")


class DeletedRevisions(Collection):
    PROPERTIES = {'ids', 'flags', 'timestamp', 'user', 'userid', 'size',
                  'sha1', 'contentmodel', 'comment', 'parsedcomment', 'content',
                  'tags'}

    # TODO:
    # This is *not* the right way to do this, but it should work for all queries.
    MAX_REVISIONS = 500

    def get(self, rev_id, *args, **kwargs):

        rev_id = int(rev_id)

        revs = list(self.query(revids={rev_id}, **kwargs))

        if len(revs) < 1:
            raise KeyError(rev_id)
        else:
            return revs[0]

    def query(self, *args, limit=sys.maxsize, **kwargs):
        """
        Queries deleted revisions.
        See https://www.mediawiki.org/wiki/API:Deletedrevs

        :Parameters:
            titles : set(str)
                A set of page names to query (note that namespace prefix is expected)
            start : :class:`mw.Timestamp`
                A timestamp to start querying from
            end : :class:`mw.Timestamp`
                A timestamp to end querying
            from_title : str
                A title from which to start querying (alphabetically)
            to_title : str
                A title from which to stop querying (alphabetically)
            prefix : str
                A title prefix to match on
            drcontinue : str
                When more results are available, use this to continue (3) Note: may only work if drdir is set to newer.
            unique : bool
                List only one revision for each page
            tag : str
                Only list revision tagged with this tag
            user : str
                Only list revisions saved by this user_text
            excludeuser : str
                Do not list revision saved by this user_text
            namespace : int
                Only list pages in this namespace (id)
            limit : int
                Limit the number of results
            direction : str
                "newer" or "older"
            properties : set(str)
                A list of properties to include in the results:


                * ids            - The ID of the revision.
                * flags          - Revision flags (minor).
                * timestamp      - The timestamp of the revision.
                * user           - User that made the revision.
                * userid         - User ID of the revision creator.
                * size           - Length (bytes) of the revision.
                * sha1           - SHA-1 (base 16) of the revision.
                * contentmodel   - Content model ID of the revision.
                * comment        - Comment by the user for the revision.
                * parsedcomment  - Parsed comment by the user for the revision.
                * content        - Text of the revision.
                * tags           - Tags for the revision.
        """
        # `limit` means something diffent here
        kwargs['limit'] = min(limit, self.MAX_REVISIONS)
        revisions_yielded = 0
        done = False
        while not done and revisions_yielded <= limit:
            rev_docs, query_continue = self._query(*args, **kwargs)
            for doc in rev_docs:
                yield doc
                revisions_yielded += 1
                if revisions_yielded >= limit:
                    break

            if query_continue != "" and len(rev_docs) > 0:
                kwargs['query_continue'] = query_continue
            else:
                done = True

    def _query(self, titles=None, pageids=None, revids=None,
               start=None, end=None, query_continue=None, unique=None, tag=None,
               user=None, excludeuser=None, namespace=None, limit=None,
               properties=None, direction=None):

        params = {
            'action': "query",
            'prop': "deletedrevisions"
        }

        params['titles'] = self._items(titles)
        params['pageids'] = self._items(pageids)
        params['revids'] = self._items(revids)
        params['drvprop'] = self._items(properties, levels=self.PROPERTIES)
        params['drvlimit'] = none_or(limit, int)
        params['drvstart'] = self._check_timestamp(start)
        params['drvend'] = self._check_timestamp(end)

        params['drvdir'] = self._check_direction(direction)
        params['drvuser'] = none_or(user, str)
        params['drvexcludeuser'] = none_or(excludeuser, int)
        params['drvtag'] = none_or(tag, str)
        params.update(query_continue or {'continue': ""})

        doc = self.session.get(params)
        doc_copy = dict(doc)

        try:
            if 'continue' in doc:
                query_continue = doc['continue']
            else:
                query_continue = ''

            pages = doc['query']['pages'].values()
            rev_docs = []

            for page_doc in pages:
                page_rev_docs = page_doc.get('deletedrevisions', [])

                try: del page_doc['deletedrevisions']
                except KeyError: pass

                for rev_doc in page_rev_docs:
                    rev_doc['page'] = page_doc

                rev_docs.extend(page_rev_docs)

            return rev_docs, query_continue

        except KeyError as e:
            raise MalformedResponse(str(e), doc)
