import logging

from ...util import none_or
from ..errors import MalformedResponse
from .collection import Collection

logger = logging.getLogger("mw.api.collections.users")


class Users(Collection):
    """
    A collection of information about users
    """

    PROPERTIES = {'blockinfo', 'implicitgroups', 'groups', 'registration',
                  'emailable', 'editcount', 'gender'}

    SHOW = {'minor', '!minor', 'patrolled', '!patrolled'}

    MAX_REVISIONS = 50

    def query(self, *args, **kwargs):
        """
        Get a user's metadata.
        See `<https://www.mediawiki.org/wiki/API:Users>`_

        :Parameters:
            users : str
                The usernames of the users to be retrieved.
            
            properties : set(str)
                Include additional pieces of information

                blockinfo      - Tags if the user is blocked, by whom, and
                                 for what reason
                groups         - Lists all the groups the user(s) belongs to
                implicitgroups - Lists all the groups a user is automatically
                                 a member of
                rights         - Lists all the rights the user(s) has
                editcount      - Adds the user's edit count
                registration   - Adds the user's registration timestamp
                emailable      - Tags if the user can and wants to receive
                                 email through [[Special:Emailuser]]
                gender         - Tags the gender of the user. Returns "male",
                                 "female", or "unknown"
        """
        done = False
        while not done:

            us_docs, query_continue = self._query(*args, **kwargs)

            for doc in us_docs:
                yield doc

            if query_continue is None or len(us_docs) == 0:
                done = True
            else:
                kwargs['query_continue'] = query_continue

    def _query(self, users, query_continue=None, properties=None):

        params = {
            'action': "query",
            'list': "users"
        }
        params['ususers'] = self._items(users, type=str)
        params['usprop'] = self._items(properties, levels=self.PROPERTIES)
        if query_continue is not None:
            params.update(query_continue)

        doc = self.session.get(params)
        try:
            if 'query-continue' in doc:
                query_continue = doc['query-continue']['users']
            else:
                query_continue = None

            us_docs = doc['query']['users']

            return us_docs, query_continue

        except KeyError as e:
            raise MalformedResponse(str(e), doc)
