from nose.tools import eq_

from ..namespace import Namespace

def test_namespace():
	
	namespace = Namespace(10, ['Foo', 'Bar'])
	
	eq_(namespace.id, 10)
	eq_(namespace.names, {'Foo', 'Bar'})
	eq_(namespace.canonical, "Foo")
	
	
	namespace = Namespace(11, ['foo', 'bar'], 'bar')
	
	eq_(namespace.id, 11)
	eq_(namespace.names, {'Foo', 'Bar'})
	eq_(namespace.canonical, "Bar")
	
