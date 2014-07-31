"""
Demonstrates title normalization and parsing.
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.getcwd()))

from mw.api import Session
from mw.lib import title

# Normalize titles
title.normalize("foo bar")
# > "Foo_bar"

# Construct a title parser from the API
api_session = Session("https://en.wikipedia.org/w/api.php")
parser = title.Parser.from_api(api_session)

# Handles normalization
parser.parse("user:epochFail")
# > 2, "EpochFail"

# Handles namespace aliases
parser.parse("WT:foobar")
# > 5, "Foobar"
