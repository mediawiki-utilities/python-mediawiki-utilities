from difflib import SequenceMatcher

from . import tokenization, difference

TOKENIZE = tokenization.simple_split

DIFF = difference.sequence_matcher
