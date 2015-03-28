import logging

from ..util import api
from .collections import (DeletedRevisions, Pages, RecentChanges, Revisions,
                          SiteInfo, UserContribs, Users)
from .errors import APIError, AuthenticationError, MalformedResponse

logger = logging.getLogger("mw.api.session")

DEFAULT_USER_AGENT = "MediaWiki-Utilities"
"""
The default User-Agent to be sent with requests to the API.
"""

class Session(api.Session):
    """
    Represents a connection to a MediaWiki API.

    Cookies and other session information is preserved.

    :Parameters:
        uri : str
            The base URI for the API to use.  Usually ends in "api.php"
        user_agent : str
            The User-Agent to be sent with requests.  Will raise a warning if
            left to default value.
    """

    def __init__(self, uri, *args, user_agent=DEFAULT_USER_AGENT, **kwargs):
        """
        Constructs a new :class:`Session`.
        """

        if user_agent == DEFAULT_USER_AGENT:
            logger.warning("Sending requests with default User-Agent.  "  +
                           "Set 'user_agent' on api.Session to quiet this " +
                           "message.")

        if 'headers' in kwargs:
            kwargs['headers']['User-Agent'] = str(user_agent)
        else:
            kwargs['headers'] = {'User-Agent': str(user_agent)}

        super().__init__(uri, *args, **kwargs)

        self.pages = Pages(self)
        """
        An instance of :class:`mw.api.Pages`.
        """

        self.revisions = Revisions(self)
        """
        An instance of :class:`mw.api.Revisions`.
        """

        self.recent_changes = RecentChanges(self)
        """
        An instance of :class:`mw.api.RecentChanges`.
        """

        self.site_info = SiteInfo(self)
        """
        An instance of :class:`mw.api.SiteInfo`.
        """

        self.user_contribs = UserContribs(self)
        """
        An instance of :class:`mw.api.UserContribs`.
        """

        self.users = Users(self)
        """
        An instance of :class:`mw.api.Users`.
        """

        self.deleted_revisions = DeletedRevisions(self)
        """
        An instance of :class:`mw.api.DeletedRevisions`.
        """

    def login(self, username, password, token=None):
        """
        Performs a login operation.  This method usually makes two requests to
        API -- one to get a token and one to use the token to log in.  If
        authentication fails, this method will throw an
        :class:`.errors.AuthenticationError`.

        :Parameters:
            username : str
                Your username
            password : str
                Your password

        :Returns:
            The response in a json :py:class:`dict`
        """

        doc = self.post(
            {
                'action': "login",
                'lgname': username,
                'lgpassword': password,
                'lgtoken': token, # If None, we'll be getting a token
            }
        )


        try:
            if doc['login']['result'] == "Success":
                return doc
            elif doc['login']['result'] == "NeedToken":

                if token is not None:
                    # Woops.  We've been here before.  Better error out.
                    raise AuthenticationError(doc)
                else:
                    token = doc['login']['token']
                    return self.login(username, password, token=token)
            else:
                raise AuthenticationError(doc)

        except KeyError as e:
            raise MalformedResponse(e.message, doc)


    def request(self, type, params, **kwargs):
        params.update({'format': "json"})

        doc = super().request(type, params, **kwargs).json()

        if 'error' in doc:
            raise APIError(doc)

        return doc
