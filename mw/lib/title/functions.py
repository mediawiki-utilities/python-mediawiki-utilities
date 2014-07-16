def normalize(title):
    """
    Normalizes a page title to the database format.  E.g. spaces are converted
    to underscores and the first character in the title is converted to
    upper-case.

    :Parameters:
        title : str
            A page title
    :Returns:
        The normalized title.
    :Example:
        >>> from mw.lib import title
        >>>
        >>> title.normalize("foo bar")
        'Foo_bar'

    """
    if title is None:
        return title
    else:
        if len(title) > 0:
            return (title[0].upper() + title[1:]).replace(" ", "_")
        else:
            return ""
