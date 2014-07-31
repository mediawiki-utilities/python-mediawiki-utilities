import io

from nose.tools import eq_
from ....types import Timestamp
from ..iterator import Iterator


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
  <page>
    <title>Bar</title>
    <ns>1</ns>
    <id>2</id>
    <redirect title="Computer accessibility" />
    <restrictions>edit=sysop:move=sysop</restrictions>
    <revision>
      <id>3</id>
      <timestamp>2004-08-11T09:04:08Z</timestamp>
      <contributor>
        <ip>222.152.210.22</ip>
      </contributor>
      <text xml:space="preserve">Revision 3 text</text>
      <sha1>g9chqqg94myzq11c56ixvq7o1yg75n9</sha1>
      <model>wikitext</model>
      <format>text/x-wiki</format>
    </revision>
    <revision>
      <id>4</id>
      <timestamp>2004-08-12T09:04:08Z</timestamp>
      <text xml:space="preserve">Revision 4 text</text>
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

    page = next(dump)
    eq_(page.title, "Bar")
    eq_(page.namespace, 1)
    eq_(page.id, 2)
    eq_(page.redirect.title, "Computer accessibility")
    eq_(page.restrictions, ["edit=sysop:move=sysop"])

    revision = next(page)
    eq_(revision.id, 3)
    eq_(revision.timestamp, Timestamp("2004-08-11T09:04:08Z"))
    eq_(revision.contributor.id, None)
    eq_(revision.contributor.user_text, "222.152.210.22")
    eq_(revision.text, "Revision 3 text")
    eq_(revision.sha1, "g9chqqg94myzq11c56ixvq7o1yg75n9")
    eq_(revision.comment, None)
    eq_(revision.model, "wikitext")
    eq_(revision.format, "text/x-wiki")

    revision = next(page)
    eq_(revision.id, 4)
    eq_(revision.timestamp, Timestamp("2004-08-12T09:04:08Z"))
    eq_(revision.contributor, None)
    eq_(revision.text, "Revision 4 text")
    eq_(revision.sha1, "6ixvq7o1yg75n9g9chqqg94myzq11c5")
    eq_(revision.comment, None)
    eq_(revision.model, "wikitext")
    eq_(revision.format, "text/x-wiki")


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
    eq_(revision.text, "Revision 3 text")
    eq_(revision.sha1, "g9chqqg94myzq11c56ixvq7o1yg75n9")
    eq_(revision.comment, None)
    eq_(revision.model, "wikitext")
    eq_(revision.format, "text/x-wiki")


def test_serialization():
    f = io.StringIO(SAMPLE_XML)

    dump = Iterator.from_file(f)

    eq_(dump, Iterator.deserialize(dump.serialize()))
