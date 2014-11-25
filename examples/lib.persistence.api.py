import pprint
import re

from mw.api import Session
from mw.lib import persistence

session = Session("https://en.wikipedia.org/w/api.php")

rev, tokens_added, future_revs = persistence.api.score(session, 560561013,
                                                       properties={'user'})

words_re = re.compile("\w+", re.UNICODE)

print("Words added")
for token in tokens_added:
    if words_re.search(token.text):
        print("'{0}' survived:".format(token.text))
        for frev in token.revisions:
            print("\t{revid} by {user}".format(**frev))
