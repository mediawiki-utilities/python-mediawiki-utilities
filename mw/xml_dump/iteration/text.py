from ...types import serializable
from ...util import none_or


class Text(str, serializable.Type):
    """
    Revision text content.  This class behaves identically to
    :class:`str` except that it takes and stores an additional set of parameters.

    **deleted**
        Was the text deleted? : `bool`
    **xml_space**
        What to do with extra whitespace? : `str`
    **id**
        TODO: ??? : `int` | `None`
    **bytes**
        TODO: ??? : `int` | `None`

    >>> from mw.xml_dump import Text
    >>>
    >>> t = Text("foo")
    >>> t == "foo"
    True
    >>> t.deleted
    False
    >>> t.xml_space
    'preserve'
    """

    def __new__(cls, string_or_text="", deleted=False, xml_space="preserve", id=None, bytes=None):
        if isinstance(string_or_text, cls):
            return string_or_text
        else:
            inst = super().__new__(cls, string_or_text)
            inst.initialize(string_or_text, deleted, xml_space, id, bytes)
            return inst

    def initialize(self, string, deleted, xml_space, id, bytes):
        self.deleted = bool(deleted)
        self.xml_space = none_or(xml_space, str)
        self.id = none_or(id, int)
        self.bytes = none_or(bytes, int)

    def __str__(self):
        return str.__str__(self)

    def __repr__(self):
        return "{0}({1})".format(
            self.__class__.__name__,
            ", ".join([
                str.__repr__(self),
                "deleted={0}".format(repr(self.deleted))
            ])
        )

    def serialize(self):
        return {
            "string_or_text": str(self),
            "deleted": self.deleted,
            "xml_space": self.xml_space,
            "id": self.id,
            "bytes": self.bytes
        }

    @classmethod
    def from_element(cls, e):
        content = e.text or ""
        return cls(
            content,
            deleted=e.attr('deleted', False),
            xml_space=e.attr('xml:space'),
            id=e.attr('id'),
            bytes=e.attr('bytes')
        )
