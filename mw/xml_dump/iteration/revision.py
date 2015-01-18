from ...types import serializable, Timestamp
from ...util import none_or
from .comment import Comment
from .contributor import Contributor
from .text import Text
from .util import consume_tags


class Revision(serializable.Type):
    """
    Revision meta data.
    """
    __slots__ = ('id', 'timestamp', 'contributor', 'minor', 'comment', 'text',
                 'bytes', 'sha1', 'parent_id', 'model', 'format',
                 'beginningofpage')

    TAG_MAP = {
        'id': lambda e: int(e.text),
        'timestamp': lambda e: Timestamp(e.text),
        'contributor': lambda e: Contributor.from_element(e),
        'minor': lambda e: True,
        'comment': lambda e: Comment.from_element(e),
        'text': lambda e: Text.from_element(e),
        'sha1': lambda e: str(e.text),
        'parentid': lambda e: int(e.text),
        'model': lambda e: str(e.text),
        'format': lambda e: str(e.text)
    }

    def __init__(self, id, timestamp, contributor=None, minor=None,
                 comment=None, text=None, bytes=None, sha1=None,
                 parent_id=None, model=None, format=None,
                 beginningofpage=False):
        self.id = none_or(id, int)
        """
        Revision ID : `int`
        """

        self.timestamp = none_or(timestamp, Timestamp)
        """
        Revision timestamp : :class:`mw.Timestamp`
        """

        self.contributor = none_or(contributor, Contributor.deserialize)
        """
        Contributor meta data : :class:`~mw.xml_dump.Contributor` | `None`
        """

        self.minor = False or none_or(minor, bool)
        """
        Is revision a minor change? : `bool`
        """

        self.comment = none_or(comment, Comment)
        """
        Comment left with revision : :class:`~mw.xml_dump.Comment` (behaves like `str`, with additional members)
        """

        self.text = none_or(text, Text)
        """
        Content of text : :class:`~mw.xml_dump.Text` (behaves like `str`, with additional members)
        """

        self.bytes = none_or(bytes, int)
        """
        Number of bytes of content : `str`
        """

        self.sha1 = none_or(sha1, str)
        """
        sha1 hash of the content : `str`
        """

        self.parent_id = none_or(parent_id, int)
        """
        Revision ID of preceding revision : `int` | `None`
        """

        self.model = none_or(model, str)
        """
        TODO: ??? : `str`
        """

        self.format = none_or(format, str)
        """
        TODO: ??? : `str`
        """

        self.beginningofpage = bool(beginningofpage)
        """
        Is the first revision of a page : `bool`
        Used to identify the first revision of a page when using Wikihadoop
        revision pairs.  Otherwise is always set to False.  Do not expect to use
        this when processing an XML dump directly.
        """

    @classmethod
    def from_element(cls, element):
        values = consume_tags(cls.TAG_MAP, element)

        return cls(
            values.get('id'),
            values.get('timestamp'),
            values.get('contributor'),
            values.get('minor') is not None,
            values.get('comment'),
            values.get('text'),
            values.get('bytes'),
            values.get('sha1'),
            values.get('parentid'),
            values.get('model'),
            values.get('format'),
            element.attr('beginningofpage') is not None
                    # For Wikihadoop.
                    # Probably never used by anything, ever.
        )
