from . import tokenization, difference

TOKENIZE = tokenization.wikitext_split
"""
The standard tokenizing function.
"""

DIFF = difference.sequence_matcher
"""
The standard diff function
"""
