import logging
import sys

from ...util import none_or
from ..errors import MalformedResponse
from .collection import Collection


logger = logging.getLogger("mw.api.collections.deletedrevs")


class DeletedRevs(Collection):
    PROPERTIES = {'revid', 'parentid', 'user', 'userid', 'comment',
                  'parsedcomment', 'minor', 'len', 'sha1', 'content', 'token',
                  'tags'}

    # TODO:
    # This is *not* the right way to do this, but it should work for all queries.
    MAX_REVISIONS = 500

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

                * revid          - Adds the revision ID of the deleted revision
                * parentid       - Adds the revision ID of the previous revision to the page
                * user           - Adds the user who made the revision
                * userid         - Adds the user ID whom made the revision
                * comment        - Adds the comment of the revision
                * parsedcomment  - Adds the parsed comment of the revision
                * minor          - Tags if the revision is minor
                * len            - Adds the length (bytes) of the revision
                * sha1           - Adds the SHA-1 (base 16) of the revision
                * content        - Adds the content of the revision
                * token          - Gives the edit token
                * tags           - Tags for the revision
        """
        # `limit` means something diffent here
        kwargs['limit'] = min(limit, self.MAX_REVISIONS)
        revisions_yielded = 0
        done = False
        while not done and revisions_yielded <= limit:
            rev_docs, drcontinue = self._query(*args, **kwargs)
            for doc in rev_docs:
                yield doc
                revisions_yielded += 1
                if revisions_yielded >= limit:
                    break

            if drcontinue is not None and len(rev_docs) > 0:
                kwargs['drcontinue'] = drcontinue
            else:
                done = True

    def _query(self, titles=None,
               start=None, end=None, from_title=None, to_title=None,
               prefix=None, drcontinue=None, unique=None, tag=None,
               user=None, excludeuser=None, namespace=None, limit=None,
               properties=None, direction=None):

        params = {
            'action': "query",
            'list': "deletedrevs"
        }

        params['titles'] = self._items(titles)
        params['drprefix'] = none_or(prefix, str)
        params['drfrom'] = none_or(from_title, str)
        params['drto'] = none_or(to_title, str)

        params['drprop'] = self._items(properties, levels=self.PROPERTIES)
        params['drlimit'] = none_or(limit, int)
        params['drstart'] = str(Timestamp(start))
        params['drend'] = str(Timestamp(end))

        params['drdir'] = self._check_direction(direction)
        params['druser'] = none_or(user, str)
        params['drexcludeuser'] = none_or(excludeuser, int)
        params['drtag'] = none_or(tag, str)
        params['drcontinue'] = none_or(drcontinue, str)

        doc = self.session.get(params)

        try:
            if 'query-continue' in doc:
                drcontinue = doc['query-continue']['deletedrevs']['drcontinue']
            else:
                drcontinue = None

            pages = doc['query']['deletedrevs']
            rev_docs = []

            for page_doc in pages:
                page_rev_docs = page_doc['revisions']
                del page_doc['revisions']

                for rev_doc in page_rev_docs:
                    rev_doc['page'] = page_doc

                rev_docs.extend(page_rev_docs)

            return rev_docs, drcontinue

        except KeyError as e:
            print(doc)
            raise MalformedResponse(str(e), doc)
