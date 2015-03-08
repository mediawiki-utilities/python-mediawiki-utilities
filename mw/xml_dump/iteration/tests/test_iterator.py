import io

from nose.tools import eq_, assert_is_instance

from ....types import Timestamp
from ..iterator import Iterator
from ..comment import Comment
from ..text import Text
from ..revision import Revision
from ..page import Page


SAMPLE_XML = """
<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.8/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http
://www.mediawiki.org/xml/export-0.8/ http://www.mediawiki.org/xml/export-0.8.xsd" version="0.8" xml:lang="en">
  <siteinfo>
    <sitename>Wikipedia</sitename>
    <base>http://en.wikipedia.org/wiki/Main_Page</base>
    <generator>MediaWiki 1.22wmf2</generator>
    <case>first-letter</case>
    <namespaces>
      <namespace key="0" case="first-letter" />
      <namespace key="1" case="first-letter">Talk</namespace>
    </namespaces>
  </siteinfo>
  <page>
    <title>Foo</title>
    <ns>0</ns>
    <id>1</id>
    <revision beginningofpage="true">
      <id>1</id>
      <timestamp>2004-08-09T09:04:08Z</timestamp>
      <contributor>
        <username>Gen0cide</username>
        <id>92182</id>
      </contributor>
      <text xml:space="preserve" bytes="234" id="55">Revision 1 text</text>
      <sha1>g9chqqg94myzq11c56ixvq7o1yg75n9</sha1>
      <model>wikitext</model>
      <format>text/x-wiki</format>
    </revision>
    <revision>
      <id>2</id>
      <timestamp>2004-08-10T09:04:08Z</timestamp>
      <contributor>
        <ip>222.152.210.109</ip>
      </contributor>
      <text xml:space="preserve" bytes="235" id="56">Revision 2 text</text>
      <sha1>g9chqqg94myzq11c56ixvq7o1yg75n9</sha1>
      <model>wikitext</model>
      <comment>Comment 2</comment>
      <format>text/x-wiki</format>
    </revision>
  </page>
  <page>
    <title>Bar</title>
    <ns>1</ns>
    <id>2</id>
    <redirect title="Computer accessibility" />
    <restrictions>edit=sysop:move=sysop</restrictions>
    <revision beginningofpage="true">
      <id>3</id>
      <timestamp>2004-08-11T09:04:08Z</timestamp>
      <contributor>
        <ip>222.152.210.22</ip>
      </contributor>
      <text xml:space="preserve" bytes="236" id="57">Revision 3 text</text>
      <sha1>g9chqqg94myzq11c56ixvq7o1yg75n9</sha1>
      <model>wikitext</model>
      <format>text/x-wiki</format>
    </revision>
    <revision>
      <id>4</id>
      <timestamp>2004-08-12T09:04:08Z</timestamp>
      <text id="58" bytes="237" />
      <sha1>6ixvq7o1yg75n9g9chqqg94myzq11c5</sha1>
      <model>wikitext</model>
      <format>text/x-wiki</format>
    </revision>
  </page>
</mediawiki>"""


def test_complete():
    f = io.StringIO(SAMPLE_XML)

    dump = Iterator.from_file(f)
    eq_([0, 1], list(ns.id for ns in dump.namespaces))

    page = next(dump)
    eq_(page.title, "Foo")
    eq_(page.namespace, 0)
    eq_(page.id, 1)
    eq_(page.redirect, None)
    eq_(page.restrictions, [])

    revision = next(page)
    eq_(revision.id, 1)
    eq_(revision.timestamp, Timestamp("2004-08-09T09:04:08Z"))
    eq_(revision.contributor.id, 92182)
    eq_(revision.contributor.user_text, "Gen0cide")
    assert_is_instance(revision.text, Text)
    eq_(revision.text, "Revision 1 text")
    eq_(revision.text.bytes, 234)
    eq_(revision.text.id, 55)
    eq_(revision.text, "Revision 1 text")
    eq_(revision.sha1, "g9chqqg94myzq11c56ixvq7o1yg75n9")
    eq_(revision.comment, None)
    eq_(revision.model, "wikitext")
    eq_(revision.format, "text/x-wiki")
    eq_(revision.beginningofpage, True)

    revision = next(page)
    eq_(revision.id, 2)
    eq_(revision.timestamp, Timestamp("2004-08-10T09:04:08Z"))
    eq_(revision.contributor.id, None)
    eq_(revision.contributor.user_text, "222.152.210.109")
    eq_(revision.text, "Revision 2 text")
    eq_(revision.text.bytes, 235)
    eq_(revision.text.id, 56)
    eq_(revision.sha1, "g9chqqg94myzq11c56ixvq7o1yg75n9")
    assert_is_instance(revision.comment, Comment)
    eq_(revision.comment, "Comment 2")
    eq_(revision.model, "wikitext")
    eq_(revision.format, "text/x-wiki")
    eq_(revision.beginningofpage, False)

    page = next(dump)
    assert_is_instance(page, Page)
    eq_(page.title, "Bar")
    eq_(page.namespace, 1)
    eq_(page.id, 2)
    eq_(page.redirect.title, "Computer accessibility")
    eq_(page.restrictions, ["edit=sysop:move=sysop"])

    revision = next(page)
    assert_is_instance(revision, Revision)
    eq_(revision.id, 3)
    eq_(revision.timestamp, Timestamp("2004-08-11T09:04:08Z"))
    eq_(revision.contributor.id, None)
    eq_(revision.contributor.user_text, "222.152.210.22")
    assert_is_instance(revision.text, Text)
    eq_(revision.text.bytes, 236)
    eq_(revision.text.id, 57)
    eq_(revision.text, "Revision 3 text")
    eq_(revision.sha1, "g9chqqg94myzq11c56ixvq7o1yg75n9")
    eq_(revision.comment, None)
    eq_(revision.model, "wikitext")
    eq_(revision.format, "text/x-wiki")
    assert_is_instance(str(page), str)

    revision = next(page)
    assert_is_instance(revision, Revision)
    eq_(revision.id, 4)
    eq_(revision.timestamp, Timestamp("2004-08-12T09:04:08Z"))
    eq_(revision.contributor, None)
    assert_is_instance(revision.text, Text)
    eq_(revision.text.bytes, 237)
    eq_(revision.text.id, 58)
    eq_(revision.text, "")
    eq_(revision.sha1, "6ixvq7o1yg75n9g9chqqg94myzq11c5")
    eq_(revision.comment, None)
    eq_(revision.model, "wikitext")
    eq_(revision.format, "text/x-wiki")
    assert_is_instance(str(revision), str)


def test_skipping():
    f = io.StringIO(SAMPLE_XML)

    dump = Iterator.from_file(f)

    page = next(dump)
    eq_(page.title, "Foo")
    eq_(page.namespace, 0)
    eq_(page.id, 1)

    page = next(dump)
    eq_(page.title, "Bar")
    eq_(page.namespace, 1)
    eq_(page.id, 2)

    revision = next(page)
    eq_(revision.id, 3)
    eq_(revision.timestamp, Timestamp("2004-08-11T09:04:08Z"))
    eq_(revision.contributor.id, None)
    eq_(revision.contributor.user_text, "222.152.210.22")
    assert_is_instance(revision.text, Text)
    eq_(revision.text, "Revision 3 text")
    eq_(revision.sha1, "g9chqqg94myzq11c56ixvq7o1yg75n9")
    eq_(revision.comment, None)
    eq_(revision.model, "wikitext")
    eq_(revision.format, "text/x-wiki")


def test_serialization():
    f = io.StringIO(SAMPLE_XML)

    dump = Iterator.from_file(f)

    eq_(dump, Iterator.deserialize(dump.serialize()))

def test_from_page_xml():
    page_xml = """
    <page>
      <title>Foo</title>
      <ns>0</ns>
      <id>1</id>
      <revision>
        <id>1</id>
        <timestamp>2004-08-09T09:04:08Z</timestamp>
        <contributor>
          <username>Gen0cide</username>
          <id>92182</id>
        </contributor>
        <text xml:space="preserve">Revision 1 text</text>
        <sha1>g9chqqg94myzq11c56ixvq7o1yg75n9</sha1>
        <model>wikitext</model>
        <format>text/x-wiki</format>
      </revision>
      <revision>
        <id>2</id>
        <timestamp>2004-08-10T09:04:08Z</timestamp>
        <contributor>
          <ip>222.152.210.109</ip>
        </contributor>
        <text xml:space="preserve">Revision 2 text</text>
        <sha1>g9chqqg94myzq11c56ixvq7o1yg75n9</sha1>
        <model>wikitext</model>
        <comment>Comment 2</comment>
        <format>text/x-wiki</format>
      </revision>
    </page>
    """

    dump = Iterator.from_page_xml(io.StringIO(page_xml))

    # You have a `namespaces`, but it's empty.
    eq_(dump.namespaces, [])

    page = next(dump)
    eq_(page.title, "Foo")
    eq_(page.namespace, 0)
    eq_(page.id, 1)

    revision = next(page)
    eq_(revision.id, 1)
    eq_(revision.timestamp, Timestamp("2004-08-09T09:04:08Z"))
    eq_(revision.contributor.id, 92182)
    eq_(revision.contributor.user_text, "Gen0cide")
    eq_(revision.text, "Revision 1 text")
    eq_(revision.sha1, "g9chqqg94myzq11c56ixvq7o1yg75n9")
    eq_(revision.comment, None)
    eq_(revision.model, "wikitext")
    eq_(revision.format, "text/x-wiki")

    revision = next(page)
    eq_(revision.id, 2)
    eq_(revision.timestamp, Timestamp("2004-08-10T09:04:08Z"))
    eq_(revision.contributor.id, None)
    eq_(revision.contributor.user_text, "222.152.210.109")
    eq_(revision.text, "Revision 2 text")
    eq_(revision.sha1, "g9chqqg94myzq11c56ixvq7o1yg75n9")
    eq_(revision.comment, "Comment 2")
    eq_(revision.model, "wikitext")
    eq_(revision.format, "text/x-wiki")
