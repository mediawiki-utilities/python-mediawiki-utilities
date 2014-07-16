class Token:
    """
    Represents a chunk of text and the revisions of a page that it survived.
    """
    __slots__ = ('text', 'revisions')

    def __init__(self, text, revisions=None):
        self.text = text
        """
        The text of the token.
        """

        self.revisions = revisions if revisions is not None else []
        """
        The meta data for the revisions that the token has appeared within.
        """

    def persist(self, revision):
        self.revisions.append(revision)

    def __repr__(self):
        return "{0}({1})".format(
            self.__class__.__name__,
            ", ".join([
                "text={0}".format(repr(self.text)),
                "revisions={0}".format(repr(self.revisions))
            ])
        )


class Tokens(list):
    """
    Represents a :class:`list` of :class:`~mw.lib.persistence.Token` with some
    useful helper functions.

    :Example:

        >>> from mw.lib.persistence import Token, Tokens
        >>>
        >>> tokens = Tokens()
        >>> tokens.append(Token("foo"))
        >>> tokens.extend([Token(" "), Token("bar")])
        >>>
        >>> tokens[0]
        Token(text='foo', revisions=[])
        >>>
        >>> "".join(tokens.texts())
        'foo bar'
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def persist(self, revision):
        for token in self:
            token.persist(revision)

    def texts(self):
        for token in self:
            yield token.text

    def compare(self, new, diff):
        old = self.texts()

        return self.apply_diff(diff(old, new), self, new)

    @classmethod
    def apply_diff(cls, ops, old, new):

        tokens = cls()
        tokens_added = cls()
        tokens_removed = cls()

        for code, a_start, a_end, b_start, b_end in ops:
            if code == "insert":
                for token_text in new[b_start:b_end]:
                    token = Token(token_text)
                    tokens.append(token)
                    tokens_added.append(token)

            elif code == "replace":
                for token_text in new[b_start:b_end]:
                    token = Token(token_text)
                    tokens.append(token)
                    tokens_added.append(token)

                tokens_removed.extend(t for t in old[a_start:a_end])

            elif code == "equal":
                tokens.extend(old[a_start:a_end])
            elif code == "delete":
                tokens_removed.extend(old[a_start:a_end])

            else:
                assert False, \
                    "encounted an unrecognized operation code: " + repr(code)

        return (tokens, tokens_added, tokens_removed)
