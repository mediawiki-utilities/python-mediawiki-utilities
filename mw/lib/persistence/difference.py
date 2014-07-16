from difflib import SequenceMatcher


def sequence_matcher(old, new):
    """
    Generates a sequence of operations using :class:`difflib.SequenceMatcher`.

    :Parameters:
        old : list( `hashable` )
            Old tokens
        new : list( `hashable` )
            New tokens

    Returns:
        Minimal operations needed to convert `old` to `new`
    """
    sm = SequenceMatcher(None, list(old), list(new))
    return sm.get_opcodes()


def apply(ops, old, new):
    """
    Applies operations (delta) to copy items from `old` to `new`.

    :Parameters:
        ops : list((op, a1, a2, b1, b2))
            Operations to perform
        old : list( `hashable` )
            Old tokens
        new : list( `hashable` )
            New tokens
    :Returns:
        An iterator over elements matching `new` but copied from `old`
    """
    for code, a_start, a_end, b_start, b_end in ops:
        if code == "insert":
            for t in new[b_start:b_end]:
                yield t
        elif code == "replace":
            for t in new[b_start:b_end]:
                yield t
        elif code == "equal":
            for t in old[a_start:a_end]:
                yield t
        elif code == "delete":
            pass
        else:
            assert False, \
                "encounted an unrecognized operation code: " + repr(code)
