from ...types import serializable
from ...util import none_or

from ..errors import MalformedXML
from .revision import Revision
from .redirect import Redirect


class Page(serializable.Type):
    """
    Page meta data and a :class:`~mw.xml_dump.Revision` iterator.  Instances of
    this class can be called as iterators directly.  E.g.

    .. code-block:: python

        page = mw.xml_dump.Page( ... )

        for revision in page:
            print("{0} {1}".format(revision.id, page_id))

    """
    __slots__ = (
        'id',
        'title',
        'namespace',
        'redirect',
        'restrictions',
        'revisions'
    )

    def __init__(self, id, title, namespace, redirect, restrictions, revisions):
        self.id = none_or(id, int)
        """
        Page ID : `int`
        """

        self.title = none_or(title, str)
        """
        Page title (namespace excluded) : `str`
        """

        self.namespace = none_or(namespace, int)
        """
        Namespace ID : `int`
        """

        self.redirect = none_or(redirect, Redirect)
        """
        Page is currently redirect? : :class:`~mw.xml_dump.Redirect` | `None`
        """

        self.restrictions = serializable.List.deserialize(restrictions)
        """
        A list of page editing restrictions (empty unless restrictions are specified) : list( `str` )
        """

        # Should be a lazy generator
        self.__revisions = revisions

    def __iter__(self):
        return self.__revisions

    def __next__(self):
        return next(self.__revisions)

    @classmethod
    def load_revisions(cls, first_revision, element):
        yield Revision.from_element(first_revision)

        for sub_element in element:
            tag = sub_element.tag

            if tag == "revision":
                yield Revision.from_element(sub_element)
            else:
                raise MalformedXML("Expected to see 'revision'.  " +
                                   "Instead saw '{0}'".format(tag))

    @classmethod
    def from_element(cls, element):
        title = None
        namespace = None
        id = None
        redirect = None
        restrictions = []

        first_revision = None

        # Consume each of the elements until we see <id> which should come last.
        for sub_element in element:
            tag = sub_element.tag
            if tag == "title":
                title = sub_element.text
            elif tag == "ns":
                namespace = sub_element.text
            elif tag == "id":
                id = int(sub_element.text)
            elif tag == "redirect":
                redirect = Redirect.from_element(sub_element)
            elif tag == "restrictions":
                restrictions.append(sub_element.text)
            elif tag == "revision":
                first_revision = sub_element
                break
            # Assuming that the first revision seen marks the end of page
            # metadata.  I'm not too keen on this assumption, so I'm leaving
            # this long comment to warn whoever ends up maintaining this.
            else:
                raise MalformedXML("Unexpected tag found when processing " +
                                   "a <page>: '{0}'".format(tag))

        # Assuming that I got here by seeing a <revision> tag.  See verbose
        # comment above.
        revisions = cls.load_revisions(first_revision, element)

        return cls(id, title, namespace, redirect, restrictions, revisions)
