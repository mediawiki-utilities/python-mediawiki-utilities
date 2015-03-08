from nose.tools import eq_

from ..namespace import Namespace


def test_namespace():
    namespace = Namespace(10, "Foo", canonical="Bar", aliases={'WT'},
                          case="foobar", content=False)

    eq_(namespace.id, 10)
    eq_(namespace.name, "Foo")
    eq_(namespace.canonical, "Bar")
    eq_(namespace.aliases, {'WT'})
    eq_(namespace.case, "foobar")
    eq_(namespace.content, False)

def test_namespace_from_doc():
    
    doc = {
        "id": 0,
        "case": "first-letter",
        "*": "",
        "content": ""
    }
    
    namespace = Namespace.from_doc(doc)
    eq_(namespace.id, 0)
    eq_(namespace.name, "")
    eq_(namespace.canonical, None)
    eq_(namespace.aliases, set())
    eq_(namespace.case, "first-letter")
    eq_(namespace.content, True)
