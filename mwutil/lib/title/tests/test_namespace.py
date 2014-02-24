from nose.tools import eq_

from ..namespace import Namespace

def test_namespace():
	
	namespace = Namespace(10, ['Foo', 'Bar'])
	
	eq_(namespace.id, 10)
	eq_(namespace.names, {'Foo', 'Bar'})
	
	
	namespace = Namespace(11, ['foo', 'bar'], canonical='bar')
	
	eq_(namespace.id, 11)
	eq_(namespace.names, {'Foo', 'Bar'})
	eq_(namespace.aliases, set())
	
	
	namespace = Namespace(11, ['foo', 'bar'], canonical='bar', 
	                      aliases=['PT'], case="foobar")
	
	eq_(namespace.aliases, {'PT'})
	eq_(namespace.case, "foobar")
	
