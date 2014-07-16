from .peekable import Peekable


def sequence(*iterables, by=None, compare=None):
    if compare is not None:
        compare = compare
    elif by is not None:
        compare = lambda i1, i2: by(i1) <= by(i2)
    else:
        compare = lambda i1, i2: i1 <= i2

    iterables = [Peekable(it) for it in iterables]

    done = False
    while not done:

        next_i = None

        for i, it in enumerate(iterables):
            if not it.empty():
                if next_i is None or compare(it.peek(), iterables[next_i].peek()):
                    next_i = i

        if next_i is None:
            done = True
        else:
            yield next(iterables[next_i])
