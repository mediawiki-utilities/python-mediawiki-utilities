import logging

from ...util import none_or
from ..errors import MalformedResponse
from .collection import Collection

logger = logging.getLogger("mw.api.collections.user_contribs")


class UserContribs(Collection):
    """
    A collection of revisions indexes by user.
    """

    PROPERTIES = {'ids', 'title', 'timestamp', 'comment', 'parsedcomment',
                  'size', 'sizediff', 'flags', 'patrolled', 'tags'}

    SHOW = {'minor', '!minor', 'patrolled', '!patrolled'}

    MAX_REVISIONS = 50

    def query(self, *args, limit=None, **kwargs):
        """
        Get a user's revisions.
        See `<https://www.mediawiki.org/wiki/API:Usercontribs>`_

        :Parameters:
            limit : int
                The maximum number of contributions to return.
            start : :class:`mw.Timestamp`
                The start timestamp to return from
            end : :class:`mw.Timestamp`
                The end timestamp to return to
            user : set(str)
                The users to retrieve contributions for.  Maximum number of values 50 (500 for bots)
            userprefix : set(str)
                Retrieve contributions for all users whose names begin with this value.
            direction : str
                "newer" or "older"
            namespace : int
                Only list contributions in these namespaces
            properties :
                Include additional pieces of information

                * ids            - Adds the page ID and revision ID
                * title          - Adds the title and namespace ID of the page
                * timestamp      - Adds the timestamp of the edit
                * comment        - Adds the comment of the edit
                * parsedcomment  - Adds the parsed comment of the edit
                * size           - Adds the new size of the edit
                * sizediff       - Adds the size delta of the edit against its parent
                * flags          - Adds flags of the edit
                * patrolled      - Tags patrolled edits
                * tags           - Lists tags for the edit
            show : set(str)
                Show only items that meet thse criteria, e.g. non minor edits only: ucshow=!minor.
                NOTE: If ucshow=patrolled or ucshow=!patrolled is set, revisions older than
                $wgRCMaxAge (2592000) won't be shown

                * minor
                * !minor,
                * patrolled,
                * !patrolled,
                * top,
                * !top,
                * new,
                * !new
            tag : str
                Only list revisions tagged with this tag
            toponly : bool
                DEPRECATED! Only list changes which are the latest revision
        """
        limit = none_or(limit, int)

        revisions_yielded = 0
        done = False
        while not done:

            if limit is None:
                kwargs['limit'] = self.MAX_REVISIONS
            else:
                kwargs['limit'] = min(limit - revisions_yielded, self.MAX_REVISIONS)

            uc_docs, uccontinue = self._query(*args, **kwargs)

            for doc in uc_docs:
                yield doc
                revisions_yielded += 1

                if limit is not None and revisions_yielded >= limit:
                    done = True
                    break

            if uccontinue is None or len(uc_docs) == 0:
                done = True
            else:
                kwargs['uccontinue'] = uccontinue

    def _query(self, user=None, userprefix=None, limit=None, start=None,
               end=None, direction=None, namespace=None, properties=None,
               show=None, tag=None, toponly=None,
               uccontinue=None):

        params = {
            'action': "query",
            'list': "usercontribs"
        }
        params['uclimit'] = none_or(limit, int)
        params['ucstart'] = self._check_timestamp(start)
        params['ucend'] = self._check_timestamp(end)
        if uccontinue is not None:
            params.update(uccontinue)
        params['ucuser'] = self._items(user, type=str)
        params['ucuserprefix'] = self._items(userprefix, type=str)
        params['ucdir'] = self._check_direction(direction)
        params['ucnamespace'] = none_or(namespace, int)
        params['ucprop'] = self._items(properties, levels=self.PROPERTIES)
        params['ucshow'] = self._items(show, levels=self.SHOW)

        doc = self.session.get(params)
        try:
            if 'query-continue' in doc:
                uccontinue = doc['query-continue']['usercontribs']
            else:
                uccontinue = None

            uc_docs = doc['query']['usercontribs']

            return uc_docs, uccontinue

        except KeyError as e:
            raise MalformedResponse(str(e), doc)
