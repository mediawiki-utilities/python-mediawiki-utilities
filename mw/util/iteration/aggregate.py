from .peekable import Peekable


def group(it, by=lambda i: i):
    return aggregate(it, by)


def aggregate(it, by=lambda i: i):
    it = Peekable(it)

    def chunk(it, by):
        identifier = by(it.peek())
        while not it.empty():
            if identifier == by(it.peek()):
                yield next(it)
            else:
                break

    while not it.empty():
        yield (by(it.peek()), chunk(it, by))
