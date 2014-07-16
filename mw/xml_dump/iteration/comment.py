from ...types import serializable


class Comment(str, serializable.Type):
    """
    A revision comment.  This class behaves identically to
    :class:`str` except that it takes and stores an additional parameter
    recording whether the comment was deleted or not.

    >>> from mw.xml_dump import Comment
    >>>
    >>> c = Comment("foo")
    >>> c == "foo"
    True
    >>> c.deleted
    False

    **deleted**
        Was the comment deleted? | `bool`

    """

    def __new__(cls, string_or_comment="", deleted=False):
        if isinstance(string_or_comment, cls):
            return string_or_comment
        else:
            inst = super().__new__(cls, string_or_comment)
            inst.initialize(string_or_comment, deleted)
            return inst

    def initialize(self, string, deleted):
        self.deleted = bool(deleted)

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
            "string_or_comment": str(self),
            "deleted": self.deleted
        }

    @classmethod
    def from_element(cls, e):
        return cls(e.text, e.attr('deleted', False))
