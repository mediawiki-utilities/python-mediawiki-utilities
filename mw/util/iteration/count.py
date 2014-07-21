def count(iterable):
    """
    Consumes all items in an iterable and returns a count.
    """
    n = 0
    for item in iterable:
        n += 1
    return n
