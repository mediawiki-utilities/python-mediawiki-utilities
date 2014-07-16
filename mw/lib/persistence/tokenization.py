import re


def wikitext_split(text):
    """
    Performs the simplest possible split of latin character-based languages
    and wikitext.

    :Parameters:
        text : str
            Text to split.
    """
    return re.findall(
        r"[\w]+|\[\[|\]\]|\{\{|\}\}|\n+| +|&\w+;|'''|''|=+|\{\||\|\}|\|\-|.",
        text
    )
