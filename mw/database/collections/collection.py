class Collection:
    DIRECTIONS = {'newer', 'older'}

    def __init__(self, db):
        self.db = db

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, repr(self.db))
