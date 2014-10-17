import io

from ...types import serializable
from ...util import none_or
from ..element_iterator import ElementIterator
from ..errors import MalformedXML
from .namespace import Namespace
from .page import Page


class Iterator(serializable.Type):
    """
    XML Dump Iterator. Dump file meta data and a
    :class:`~mw.xml_dump.Page` iterator.  Instances of this class can be
    called as an iterator directly.  E.g.::

        from mw.xml_dump import Iterator

        # Construct dump file iterator
        dump = Iterator.from_file(open("example/dump.xml"))

        # Iterate through pages
        for page in dump:

            # Iterate through a page's revisions
            for revision in page:

                print(revision.id)

    """
    __slots__ = ('site_name', 'base', 'generator', 'case', 'namespaces',
                 '__pages')

    def __init__(self, site_name=None, base=None, generator=None, case=None,
                 namespaces=None, pages=None):

        self.site_name = none_or(site_name, str)
        """
        The name of the site. : str | `None` (if not specified in the XML)
        """

        self.base = none_or(base, str)
        """
        TODO: ??? : str | `None` (if not specified in the XML)
        """

        self.generator = none_or(generator, str)
        """
        TODO: ??? : str | `None` (if not specified in the XML)
        """

        self.case = none_or(case, str)
        """
        TODO: ??? : str | `None` (if not specified in the XML)
        """

        self.namespaces = none_or(namespaces, list)
        """
        A list of :class:`mw.Namespace` | `None` (if not specified in the XML)
        """

        # Should be a lazy generator of page info
        self.__pages = pages

    def __iter__(self):
        return self.__pages

    def __next__(self):
        return next(self.__pages)

    @classmethod
    def load_namespaces(cls, element):
        namespaces = []
        for sub_element in element:
            tag = sub_element.tag

            if tag == "namespace":
                namespace = Namespace.from_element(sub_element)
                namespaces.append(namespace)
            else:
                assert False, "This should never happen"

        return namespaces

    @classmethod
    def load_site_info(cls, element):

        site_name = None
        base = None
        generator = None
        case = None
        namespaces = {}

        for sub_element in element:
            if sub_element.tag == 'sitename':
                site_name = sub_element.text
            elif sub_element.tag == 'base':
                base = sub_element.text
            elif sub_element.tag == 'generator':
                generator = sub_element.text
            elif sub_element.tag == 'case':
                case = sub_element.text
            elif sub_element.tag == 'namespaces':
                namespaces = cls.load_namespaces(sub_element)

        return site_name, base, generator, case, namespaces

    @classmethod
    def load_pages(cls, element):

        for sub_element in element:
            tag = sub_element.tag

            if tag == "page":
                yield Page.from_element(sub_element)
            else:
                assert MalformedXML("Expected to see 'page'.  " +
                                    "Instead saw '{0}'".format(tag))

    @classmethod
    def from_element(cls, element):

        site_name = None
        base = None
        generator = None
        case = None
        namespaces = None

        # Consume <siteinfo>
        for sub_element in element:
            tag = sub_element.tag
            if tag == "siteinfo":
                site_name, base, generator, case, namespaces = \
                    cls.load_site_info(sub_element)
                break

        # Consume all <page>
        pages = cls.load_pages(element)

        return cls(site_name, base, generator, case, namespaces, pages)

    @classmethod
    def from_file(cls, f):
        element = ElementIterator.from_file(f)
        assert element.tag == "mediawiki"
        return cls.from_element(element)
    
    @classmethod
    def from_page_xml(cls, page_xml):
        # TODO: This is shameful
        header = """
        <mediawiki xmlns="http://www.mediawiki.org/xml/export-0.5/"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.5/
                     http://www.mediawiki.org/xml/export-0.5.xsd" version="0.5"
                   xml:lang="en">
        <siteinfo>
            <namespaces>
            </namespaces>
        </siteinfo>
        """
        
        footer = "</mediawiki>"
        
        # TODO: This is even more shameful.  We should not be concatinating a
        #       string into a StringIO.  We should be producing a legitimate
        #       TextIO thingie that streams the page XML, but programmers are
        #       lazy and RAM is cheap, so here we are.
        return cls.from_file(io.StringIO(header + page_xml + footer))
