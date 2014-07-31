from ...types import serializable
from ...util import none_or

from .util import consume_tags


class Contributor(serializable.Type):
    """
    Contributor meta data.
    """
    __slots__ = ('id', 'user_text')

    TAG_MAP = {
        'id': lambda e: int(e.text),
        'username': lambda e: str(e.text),
        'ip': lambda e: str(e.text)
    }

    def __init__(self, id, user_text):
        self.id = none_or(id, int)
        """
        User ID : int | `None` (if not specified in the XML)
        """

        self.user_text = none_or(user_text, str)
        """
        User name or IP address : str | `None` (if not specified in the XML)
        """

    @classmethod
    def from_element(cls, element):
        values = consume_tags(cls.TAG_MAP, element)

        return cls(
            values.get('id'),
            values.get('username', values.get('ip'))
        )
