from mw.lib import title


# Normalization
assert title.normalize("foo bar") == "Foo_bar"

# Parsing (namespace extration)
parser = title.Parser([title.Namespace(1, ["Talk"])])
assert parser.parse("Foo") == (0, "Foo")
assert parser.parse("Talk:Foo") == (1, "Foo")
assert parser.parse("Bar:Foo") == (0, "Bar:Foo") # Psuedo namespaces don't get split out

# Configued from API
from mw.api import API

api = API("https://en.wikipedia.org/w/api.php")

si_doc = api.siteinfo.query(properties={'namespaces'})
parser = title.Parser.from_site_info(si_doc)
assert(parser.parse("Wikipedia:Snuggle") == (4, "Snuggle")

# Configured from dump
from mw import dump


