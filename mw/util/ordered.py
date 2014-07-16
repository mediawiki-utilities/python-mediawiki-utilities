from . import autovivifying


class Circle(list):
    def __init__(self, maxsize, iterable=None):
        self._maxsize = int(maxsize)
        list.__init__(self, [None] * maxsize)
        self._size = 0
        self._pointer = 0

        if iterable is not None:
            self.extend(iterable)

    def state(self):
        return list(list.__iter__(self))

    def _internalize(self, index):
        if self._size < self._maxsize:
            return index
        else:
            return (self._pointer + index) % self._maxsize

    def __iter__(self):
        for i in range(0, self._size):
            yield list.__getitem__(self, self._internalize(i))

    def __reversed__(self):
        for i in range(self._size - 1, -1, -1):
            yield list.__getitem__(self, self._internalize(i))

    def pop(self, index=None):
        raise NotImplementedError()

    def __len__(self):
        return self._size

    def __getitem__(self, index):
        return list.__getitem__(self, self._internalize(index))

    def append(self, value):
        # Get the old value
        old_value = list.__getitem__(self, self._pointer)

        # Update internal list
        list.__setitem__(self, self._pointer, value)

        # Update state
        self._pointer = (self._pointer + 1) % self._maxsize
        self._size = min(self._maxsize, self._size + 1)

        # If we overwrote a value, yield it.
        return old_value

    def extend(self, values):
        for value in values:
            expectorate = self.append(value)
            if expectorate is not None or self._size == self._maxsize:
                yield expectorate


class HistoricalMap(autovivifying.Dict):
    '''
    A datastructure for efficiently storing and retrieving a
    limited number of historical records.

    TODO: Rename this to FIFOCache
    '''

    def __init__(self, *args, maxlen, **kwargs):
        '''Maxlen specifies the maximum amount of history to keep'''
        super().__init__(self, *args, vivifier=lambda k: [], **kwargs)

        self._circle = Circle(maxlen)  # List to preserve order for history

    def __iter__(self):
        return iter(self._circle)

    def __setitem__(self, key, value):
        '''Adds a new key-value pair. Returns any discarded values.'''

        # Add to history circle and catch expectorate
        expectorate = self._circle.append((key, value))

        autovivifying.Dict.__getitem__(self, key).append(value)

        if expectorate is not None:
            old_key, old_value = expectorate
            autovivifying.Dict.__getitem__(self, old_key).pop(0)
            if len(autovivifying.Dict.__getitem__(self, old_key)) == 0:
                autovivifying.Dict.__delitem__(self, old_key)

            return (old_key, old_value)

    def insert(self, key, value):
        return self.__setitem__(key, value)

    def __getitem__(self, key):
        if key in self:
            return autovivifying.Dict.__getitem__(self, key)[-1]
        else:
            raise KeyError(key)

    def get(self, key):
        '''Gets the most recently added value for a key'''
        return self.__getitem__(key)

    def up_to(self, key):
        '''Gets the recently inserted values up to a key'''
        for okey, ovalue in reversed(self._circle):
            if okey == key:
                break
            else:
                yield ovalue

    def last(self):
        return self.circle[-1]
