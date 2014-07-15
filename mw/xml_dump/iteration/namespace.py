from ... import types


class Namespace(types.Namespace):
    @classmethod
    def from_element(cls, element):
        return cls(
            element.attr('key'),
            element.text,
            case=element.attr('case')
        )
