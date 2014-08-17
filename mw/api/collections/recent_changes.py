import logging
import re

from ...util import none_or
from ..errors import MalformedResponse
from .collection import Collection

logger = logging.getLogger("mw.api.collections.recent_changes")


class RecentChanges(Collection):
    """
    Recent changes (revisions, page creations, registrations, moves, etc.)
    """

    RCCONTINUE = re.compile(r"([0-9]{4}-[0-9]{2}-[0-9]{2}T" +
                            r"[0-9]{2}:[0-9]{2}:[0-9]{2}Z|" +
                            r"[0-9]{14})" +
                            r"\|[0-9]+")

    PROPERTIES = {'user', 'userid', 'comment', 'timestamp', 'title',
                  'ids', 'sizes', 'redirect', 'flags', 'loginfo',
                  'tags', 'sha1'}

    SHOW = {'minor', '!minor', 'bot', '!bot', 'anon', '!anon',
            'redirect', '!redirect', 'patrolled', '!patrolled'}

    DIRECTIONS = {'newer', 'older'}

    MAX_CHANGES = 50

    def _check_rccontinue(self, rccontinue):
        if rccontinue is None:
            return None
        elif self.RCCONTINUE.match(rccontinue):
            return rccontinue
        else:
            raise TypeError(
                "rccontinue {0} is not formatted correctly ".format(rccontinue) +
                "'%Y-%m-%dT%H:%M:%SZ|<last_rcid>'"
            )

    def query(self, *args, limit=None, **kwargs):
        """
        Enumerate recent changes.
        See `<https://www.mediawiki.org/wiki/API:Recentchanges>`_

        :Parameters:
            start : :class:`mw.Timestamp`
                The timestamp to start enumerating from
            end : :class:`mw.Timestamp`
                The timestamp to end enumerating
            direction :
                "newer" or "older"
            namespace : int
                Filter log entries to only this namespace(s)
            user : str
                Only list changes by this user
            excludeuser : str
                Don't list changes by this user
            tag : str
                Only list changes tagged with this tag
            properties : set(str)
                Include additional pieces of information

                * user           - Adds the user responsible for the edit and tags if they are an IP
                * userid         - Adds the user id responsible for the edit
                * comment        - Adds the comment for the edit
                * parsedcomment  - Adds the parsed comment for the edit
                * flags          - Adds flags for the edit
                * timestamp      - Adds timestamp of the edit
                * title          - Adds the page title of the edit
                * ids            - Adds the page ID, recent changes ID and the new and old revision ID
                * sizes          - Adds the new and old page length in bytes
                * redirect       - Tags edit if page is a redirect
                * patrolled      - Tags patrollable edits as being patrolled or unpatrolled
                * loginfo        - Adds log information (logid, logtype, etc) to log entries
                * tags           - Lists tags for the entry
                * sha1           - Adds the content checksum for entries associated with a revision

            token : set(str)
                Which tokens to obtain for each change

                * patrol

            show : set(str)
                Show only items that meet this criteria. For example, to see
                only minor edits done by logged-in users, set
                show={'minor', '!anon'}.

                * minor
                * !minor
                * bot
                * !bot
                * anon
                * !anon
                * redirect
                * !redirect
                * patrolled
                * !patrolled
                * unpatrolled
            limit : int
                How many total changes to return
            type : set(str)
                Which types of changes to show

                * edit
                * external
                * new
                * log

            toponly : bool
                Only list changes which are the latest revision
            rccontinue : str
                Use this to continue loading results from where you last left off
        """
        limit = none_or(limit, int)

        changes_yielded = 0
        done = False
        while not done:

            if limit is None:
                kwargs['limit'] = self.MAX_CHANGES
            else:
                kwargs['limit'] = min(limit - changes_yielded, self.MAX_CHANGES)

            rc_docs, rccontinue = self._query(*args, **kwargs)

            for doc in rc_docs:
                yield doc
                changes_yielded += 1

                if limit is not None and changes_yielded >= limit:
                    done = True
                    break

            if rccontinue is not None and len(rc_docs) > 0:

                kwargs['rccontinue'] = rccontinue
            else:
                done = True

    def _query(self, start=None, end=None, direction=None, namespace=None,
               user=None, excludeuser=None, tag=None, properties=None,
               token=None, show=None, limit=None, type=None,
               toponly=None, rccontinue=None):

        params = {
            'action': "query",
            'list': "recentchanges"
        }

        params['rcstart'] = none_or(start, str)
        params['rcend'] = none_or(end, str)

        assert direction in {None} | self.DIRECTIONS, \
            "Direction must be one of {0}".format(self.DIRECTIONS)

        params['rcdir'] = direction
        params['rcnamespace'] = none_or(namespace, int)
        params['rcuser'] = none_or(user, str)
        params['rcexcludeuser'] = none_or(excludeuser, str)
        params['rctag'] = none_or(tag, str)
        params['rcprop'] = self._items(properties, levels=self.PROPERTIES)
        params['rctoken'] = none_or(tag, str)
        params['rcshow'] = self._items(show, levels=self.SHOW)
        params['rclimit'] = none_or(limit, int)
        params['rctype'] = none_or(type, str)
        params['rctoponly'] = none_or(toponly, bool)
        params['rccontinue'] = self._check_rccontinue(rccontinue)

        doc = self.session.get(params)

        try:
            rc_docs = doc['query']['recentchanges']

            if 'query-continue' in doc:
                rccontinue = \
                        doc['query-continue']['recentchanges']['rccontinue']
            elif len(rc_docs) > 0:
                rccontinue = "|".join([rc_docs[-1]['timestamp'],
                                       str(rc_docs[-1]['rcid'] + 1)])
            else:
                pass  # Leave it be

        except KeyError as e:
            raise MalformedResponse(str(e), doc)

        return rc_docs, rccontinue
