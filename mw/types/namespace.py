from . import serializable
from ..util import none_or


class Namespace(serializable.Type):
    """
    Namespace meta data.
    """

    __slots__ = ('id', 'name', 'aliases', 'case', 'canonical')

    def __init__(self, id, name, canonical=None, aliases=None, case=None,
                       content=False):
        
        self.id = int(id)
        """
        Namespace ID : `int`
        """

        self.name = none_or(name, str)
        """
        Namespace name : `str`
        """

        self.aliases = serializable.Set.deserialize(aliases or [], str)
        """
        Alias names : set( `str` )
        """

        self.case = none_or(case, str)
        """
        Case sensitivity : `str` | `None`
        """

        self.canonical = none_or(canonical, str)
        """
        Canonical name : `str` | `None`
        """
        
        self.content = bool(content)
        """
        Is considered a content namespace : `bool`
        """

    def __hash__(self):
        return self.id
    
    @classmethod
    def from_doc(cls, doc, aliases={}):
        """
        Constructs a namespace object from a namespace doc returned by the API
        site_info call.
        """
        return cls(
            doc['id'],
            doc['*'],
            canonical=doc.get('canonical'),
            aliases=set(aliases.get(doc['id'], [])),
            case=doc['case'],
            content='content' in doc
        )
