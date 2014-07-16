from ..util import none_or

from . import serializable


class Namespace(serializable.Type):
    """
    Namespace meta data.
    """

    __slots__ = ('id', 'name', 'aliases', 'case', 'canonical')

    def __init__(self, id, name, canonical=None, aliases=None, case=None):
        self.id = int(id)
        """
        Namespace ID : `int`
        """

        self.name = str(name)
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

    def __hash__(self):
        return self.id
