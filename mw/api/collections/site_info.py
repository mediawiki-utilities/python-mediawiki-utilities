import logging

from ..errors import MalformedResponse
from .collection import Collection

logger = logging.getLogger("mw.api.collections.site_info")


class SiteInfo(Collection):
    """
    General information about the site.
    """

    PROPERTIES = {'general', 'namespaces', 'namespacealiases',
                  'specialpagealiases', 'magicwords', 'interwikimap',
                  'dbrepllag', 'statistics', 'usergroups', 'extensions',
                  'fileextensions', 'rightsinfo', 'languages', 'skins',
                  'extensiontags', 'functionhooks', 'showhooks',
                  'variables', 'protocols'}

    FILTERIW = {'local', '!local'}

    def query(self, properties=None, filteriw=None, showalldb=None,
              numberinggroup=None, inlanguagecode=None):
        """
        General information about the site.
        See `<https://www.mediawiki.org/wiki/API:Meta#siteinfo_.2F_si>`_

        :Parameters:
            properties: set(str)
                Which sysinfo properties to get:

                * general               - Overall system information
                * namespaces            - List of registered namespaces and their canonical names
                * namespacealiases      - List of registered namespace aliases
                * specialpagealiases    - List of special page aliases
                * magicwords            - List of magic words and their aliases
                * statistics            - Returns site statistics
                * interwikimap          - Returns interwiki map (optionally filtered, (optionally localised by using siinlanguagecode))
                * dbrepllag             - Returns database server with the highest replication lag
                * usergroups            - Returns user groups and the associated permissions
                * extensions            - Returns extensions installed on the wiki
                * fileextensions        - Returns list of file extensions allowed to be uploaded
                * rightsinfo            - Returns wiki rights (license) information if available
                * restrictions          - Returns information on available restriction (protection) types
                * languages             - Returns a list of languages MediaWiki supports(optionally localised by using siinlanguagecode)
                * skins                 - Returns a list of all enabled skins
                * extensiontags         - Returns a list of parser extension tags
                * functionhooks         - Returns a list of parser function hooks
                * showhooks             - Returns a list of all subscribed hooks (contents of $wgHooks)
                * variables             - Returns a list of variable IDs
                * protocols             - Returns a list of protocols that are allowed in external links.
                * defaultoptions        - Returns the default values for user preferences.
            filteriw : str
                "local" or "!local" Return only local or only nonlocal entries of the interwiki map
            showalldb : bool
                List all database servers, not just the one lagging the most
            numberingroup : bool
                Lists the number of users in user groups
            inlanguagecode : bool
                Language code for localised language names (best effort, use CLDR extension)
  """

        siprop = self._items(properties, levels=self.PROPERTIES)

        doc = self.session.get(
            {
                'action': "query",
                'meta': "siteinfo",
                'siprop': siprop,
                'sifilteriw': filteriw,
                'sishowalldb': showalldb,
                'sinumberinggroup': numberinggroup,
                'siinlanguagecode': inlanguagecode
            }
        )

        try:
            return doc['query']
        except KeyError as e:
            raise MalformedResponse(str(e), doc)
