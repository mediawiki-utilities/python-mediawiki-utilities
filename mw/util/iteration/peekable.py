def Peekable(it):
    if isinstance(it, PeekableType):
        return it
    else:
        return PeekableType(it)


class PeekableType:
    class EMPTY:
        pass

    def __init__(self, it):
        self.it = iter(it)
        self.__cycle()

    def __iter__(self):
        return self

    def __cycle(self):
        try:
            self.lookahead = next(self.it)
        except StopIteration:
            self.lookahead = self.EMPTY

    def __next__(self):
        item = self.peek()
        self.__cycle()
        return item

    def peek(self):
        if self.empty():
            raise StopIteration()
        else:
            return self.lookahead

    def empty(self):
        return self.lookahead == self.EMPTY
