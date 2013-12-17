from nose.tools import eq_

from .. import tokenization

def test_simple_split():
	
	eq_(
		list(tokenization.simple_split("foo bar herp {{derp}}")),
		["foo", " ", "bar", " ", "herp", " ", "{{", "derp", "}}"]
	)
	