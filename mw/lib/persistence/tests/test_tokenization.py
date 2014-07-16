from nose.tools import eq_

from .. import tokenization


def test_wikitext_split():
    eq_(
        list(tokenization.wikitext_split("foo bar herp {{derp}}")),
        ["foo", " ", "bar", " ", "herp", " ", "{{", "derp", "}}"]
    )
