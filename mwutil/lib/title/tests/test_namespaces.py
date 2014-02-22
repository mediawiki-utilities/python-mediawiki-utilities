from nose.tools import eq_

from ..namespaces import Namespaces
from ..namespace import Namespace

def test_namespace():
	
	namespaces = Namespaces(
		[
			Namespace(0, [""], case="first-letter"),
			Namespace(1, ["Discuss\u00e3o"], canonical="Talk", case="first-letter"),
			Namespace(2, ["Usu\u00e1rio(a)"], canonical="User", case="first-letter")
		]
	)
	
	assert "" in namespaces
	assert "Talk" in namespaces
	assert "Usu\u00e1rio(a)" in namespaces
	assert not "Foobar" in namespaces

def test_from_site_info():
	
	namespaces = Namespaces.from_site_info(
		{
			"query": {
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
		}
	)
	
	assert "" in namespaces
	assert "Talk" in namespaces
	assert "Usu\u00e1rio(a)" in namespaces
	assert not "Foobar" in namespaces
