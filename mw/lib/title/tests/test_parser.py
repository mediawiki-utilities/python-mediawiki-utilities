from nose.tools import eq_

from ....types import Namespace

from ..parser import Parser


def test_simple():
    parser = Parser(
        [
            Namespace(0, "", case="first-letter"),
            Namespace(1, "Discuss\u00e3o", canonical="Talk", case="first-letter"),
            Namespace(2, "Usu\u00e1rio(a)", canonical="User", case="first-letter")
        ]
    )

    eq_((1, "Foo"), parser.parse("Discuss\u00e3o:Foo"))
    eq_((1, "Foo_bar"), parser.parse("Discuss\u00e3o:Foo bar"))
    eq_((0, "Herpderp:Foo_bar"), parser.parse("Herpderp:Foo bar"))


def test_from_site_info():
    parser = Parser.from_site_info(
        {
            "namespaces": {
                "0": {
                    "id": 0,
                    "case": "first-letter",
                    "*": "",
                    "content": ""
                },
                "1": {
                    "id": 1,
                    "case": "first-letter",
                    "*": "Discuss\u00e3o",
                    "subpages": "",
                    "canonical": "Talk"
                },
                "2": {
                    "id": 2,
                    "case": "first-letter",
                    "*": "Usu\u00e1rio(a)",
                    "subpages": "",
                    "canonical": "User"
                }
            }
        }
    )

    eq_((1, "Foo"), parser.parse("Discuss\u00e3o:Foo"))
    eq_((1, "Foo_bar"), parser.parse("Discuss\u00e3o:Foo bar"))
    eq_((0, "Herpderp:Foo_bar"), parser.parse("Herpderp:Foo bar"))
