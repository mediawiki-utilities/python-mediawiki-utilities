from ...types import Namespace
from ...util import autovivifying, none_or

from .functions import normalize


class Parser:
    """
    Constructs a page name parser from a set of :class:`mw.Namespace`.  Such a
    parser can be used to convert a full page name (namespace included with a
    colon; e.g, ``"Talk:Foo"``) into a namespace ID and
    :func:`mw.lib.title.normalize`'d page title (e.g., ``(1, "Foo")``).

    :Parameters:
        namespaces : set( :class:`mw.Namespace` )
    :Example:
        >>> from mw import Namespace
        >>> from mw.lib import title
        >>>
        >>> parser = title.Parser(
        ...     [
        ...             Namespace(0, "", case="first-letter"),
        ...             Namespace(1, "Discuss\u00e3o", canonical="Talk", case="first-letter"),
        ...             Namespace(2, "Usu\u00e1rio(a)", canonical="User", aliases={"U"}, case="first-letter")
        ...     ]
        ... )
        >>>
        >>> parser.parse("Discuss\u00e3o:Foo") # Using the standard name
        (1, 'Foo')
        >>> parser.parse("Talk:Foo bar") # Using the cannonical name
        (1, 'Foo_bar')
        >>> parser.parse("U:Foo bar") # Using an alias
        (2, 'Foo_bar')
        >>> parser.parse("Herpderp:Foo bar") # Psuedo namespace
        (0, 'Herpderp:Foo_bar')
    """

    def __init__(self, namespaces=None):
        namespaces = none_or(namespaces, set)

        self.ids = {}
        self.names = {}

        if namespaces is not None:
            for namespace in namespaces:
                self.add_namespace(namespace)

    def parse(self, page_name):
        """
        Parses a page name to extract the namespace.

        :Parameters:
            page_name : str
                A page name including the namespace prefix and a colon (if not Main)

        :Returns:
            A tuple of (namespace : `int`, title : `str`)
        """
        parts = page_name.split(":", 1)
        if len(parts) == 1:
            ns_id = 0
            title = normalize(page_name)
        else:
            ns_name, title = parts
            ns_name, title = normalize(ns_name), normalize(title)

            if self.contains_name(ns_name):
                ns_id = self.get_namespace(name=ns_name).id
            else:
                ns_id = 0
                title = normalize(page_name)

        return ns_id, title

    def add_namespace(self, namespace):
        """
        Adds a namespace to the parser.

        :Parameters:
            namespace : :class:`mw.Namespace`
                A namespace
        """
        self.ids[namespace.id] = namespace
        self.names[namespace.name] = namespace

        for alias in namespace.aliases:
            self.names[alias] = namespace

        if namespace.canonical is not None:
            self.names[namespace.canonical] = namespace

    def contains_name(self, name):
        return normalize(name) in self.names

    def get_namespace(self, id=None, name=None):
        """
        Gets a namespace from the parser.  Throws a :class:`KeyError` if a
        namespace cannot be found.

        :Parameters:
            id : int
                A namespace ID
            name : str
                A namespace name (standard, cannonical names and aliases
                will be searched)
        :Returns:
            A :class:`mw.Namespace`.
        """
        if id is not None:
            return self.ids[int(id)]
        else:
            return self.names[normalize(name)]

    @classmethod
    def from_site_info(cls, si_doc):
        """
        Constructs a parser from the result of a :meth:`mw.api.SiteInfo.query`.

        :Parameters:
            si_doc : dict
                The result of a site_info request.

        :Returns:
            An initialized :class:`mw.lib.title.Parser`
        """
        aliases = autovivifying.Dict(vivifier=lambda k: [])
        # get aliases
        if 'namespacealiases' in si_doc:
            for alias_doc in si_doc['namespacealiases']:
                aliases[alias_doc['id']].append(alias_doc['*'])

        namespaces = []
        for ns_doc in si_doc['namespaces'].values():
            namespaces.append(
                Namespace(
                    ns_doc['id'],
                    ns_doc['*'],
                    canonical=ns_doc.get('canonical'),
                    aliases=aliases[ns_doc['id']],
                    case=ns_doc['case']
                )
            )

        return Parser(namespaces)

    @classmethod
    def from_api(cls, session):
        """
        Constructs a parser from a :class:`mw.api.Session`

        :Parameters:
            session : :class:`mw.api.Session`
                An open API session

        :Returns:
            An initialized :class:`mw.lib.title.Parser`
        """
        si_doc = session.site_info.query(
            properties={'namespaces', 'namespacealiases'}
        )

        return cls.from_site_info(si_doc)

    @classmethod
    def from_dump(cls, dump):
        """
        Constructs a parser from a :class:`mw.xml_dump.Iterator`.  Note that
        XML database dumps do not include namespace aliases or cannonical names
        so the parser that will be constructed will only work in common cases.

        :Parameters:
            dump : :class:`mw.xml_dump.Iterator`
                An XML dump iterator

        :Returns:
            An initialized :class:`mw.lib.title.Parser`
        """
        return cls(dump.namespaces)
