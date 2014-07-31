from ...types import serializable
from ...util import none_or


class Redirect(serializable.Type):
    """
    Represents a redirect tag.

    **title**
        Full page name that this page is redirected to : `str`
    """

    def __new__(cls, redirect_or_title):
        if isinstance(redirect_or_title, cls):
            return redirect_or_title
        else:
            inst = super().__new__(cls)
            inst.initialize(redirect_or_title)
            return inst

    def __init__(self, *args, **kwargs):
        pass

    def initialize(self, title):
        self.title = none_or(title, str)

    @classmethod
    def from_element(cls, e):
        return cls(e.attr('title'))
