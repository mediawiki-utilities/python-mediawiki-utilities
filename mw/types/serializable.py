from itertools import chain


class Type:
    def __eq__(self, other):
        if other is None:
            return False
        try:
            for key in self.keys():
                if getattr(self, key) != getattr(other, key):
                    return False

            return True
        except KeyError:
            return False

    def __neq__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "%s(%s)" % (
            self.__class__.__name__,
            ", ".join(
                "%s=%r" % (k, v) for k, v in self.items()
            )
        )

    def items(self):
        for key in self.keys():
            yield key, getattr(self, key)

    def keys(self):
        return (
            key for key in
            chain(getattr(self, "__slots__", []), self.__dict__.keys())
            if key[:2] != "__"
        )

    def serialize(self):
        return dict(
            (k, self._serialize(v))
            for k, v in self.items()
        )

    def _serialize(self, value):
        if hasattr(value, "serialize"):
            return value.serialize()
        else:
            return value

    @classmethod
    def deserialize(cls, doc_or_instance):
        if isinstance(doc_or_instance, cls):
            return doc_or_instance
        else:
            return cls(**doc_or_instance)


class Dict(dict, Type):
    def serialize(self):
        return {k: self._serialize(v) for k, v in self.items()}

    @staticmethod
    def deserialize(d, value_deserializer=lambda v: v):
        if isinstance(d, Dict):
            return d
        else:
            return Dict((k, value_deserializer(v)) for k, v in d.items())


class Set(set, Type):
    def serialize(self):
        return [self._serialize(v) for v in self]

    @staticmethod
    def deserialize(s, value_deserializer=lambda v: v):

        if isinstance(s, Set):
            return s
        else:
            return Set(value_deserializer(v) for v in s)


class List(list, Type):
    def serialize(self):
        return list(self._serialize(v) for v in self)

    @staticmethod
    def deserialize(l, value_deserializer=lambda v: v):

        if isinstance(l, List):
            return l
        else:
            return List(value_deserializer(v) for v in l)
