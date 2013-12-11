from mwlib.api import API

en_api = API("https://en.wikipedia.org/w/api.php")

en_api.revisions.query(
	properties=['ids','flags','comment','tags'],
	limit=None,
	startid=None,
	endid=None,
	start=None,
	end=None,
	direction=None,
	user=None,
	excludeuser=None,
	tag=None,
	expandtemplates=None,
	generatexml=None,
	parse=None,
	section=None,
	token=None,
	query_continue=None,
	diffto=None,
	difftotext=None,
	contentformat=None
)
