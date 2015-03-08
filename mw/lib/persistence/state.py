from hashlib import sha1

from . import defaults
from .. import reverts
from .tokens import Token, Tokens


class Version:
    __slots__ = ('tokens')

    def __init__(self):
        self.tokens = None


class State:
    """
    Represents the state of word persistence in a page.
    See `<https://meta.wikimedia.org/wiki/Research:Content_persistence>`_

    :Parameters:
        tokenize : function( `str` ) --> list( `str` )
            A tokenizing function
        diff : function(list( `str` ), list( `str` )) --> list( `ops` )
            A function to perform a difference between token lists
        revert_radius : int
            a positive integer indicating the maximum revision distance that a revert can span.
        revert_detector : :class:`mw.lib.reverts.Detector`
            a revert detector to start process with
    :Example:
        >>> from pprint import pprint
        >>> from mw.lib import persistence
        >>>
        >>> state = persistence.State()
        >>>
        >>> pprint(state.process("Apples are red.", revision=1))
        ([Token(text='Apples', revisions=[1]),
          Token(text=' ', revisions=[1]),
          Token(text='are', revisions=[1]),
          Token(text=' ', revisions=[1]),
          Token(text='red', revisions=[1]),
          Token(text='.', revisions=[1])],
         [Token(text='Apples', revisions=[1]),
          Token(text=' ', revisions=[1]),
          Token(text='are', revisions=[1]),
          Token(text=' ', revisions=[1]),
          Token(text='red', revisions=[1]),
          Token(text='.', revisions=[1])],
         [])
        >>> pprint(state.process("Apples are blue.", revision=2))
        ([Token(text='Apples', revisions=[1, 2]),
          Token(text=' ', revisions=[1, 2]),
          Token(text='are', revisions=[1, 2]),
          Token(text=' ', revisions=[1, 2]),
          Token(text='blue', revisions=[2]),
          Token(text='.', revisions=[1, 2])],
         [Token(text='blue', revisions=[2])],
         [Token(text='red', revisions=[1])])
        >>> pprint(state.process("Apples are red.", revision=3)) # A revert!
        ([Token(text='Apples', revisions=[1, 2, 3]),
          Token(text=' ', revisions=[1, 2, 3]),
          Token(text='are', revisions=[1, 2, 3]),
          Token(text=' ', revisions=[1, 2, 3]),
          Token(text='red', revisions=[1, 3]),
          Token(text='.', revisions=[1, 2, 3])],
         [],
         [])
    """

    def __init__(self, tokenize=defaults.TOKENIZE, diff=defaults.DIFF,
                 revert_radius=reverts.defaults.RADIUS,
                 revert_detector=None):
        self.tokenize = tokenize
        self.diff = diff

        # Either pass a detector or the revert radius so I can make one
        if revert_detector is None:
            self.revert_detector = reverts.Detector(int(revert_radius))
        else:
            self.revert_detector = revert_detector

        # Stores the last tokens
        self.last = None

    def process(self, text, revision=None, checksum=None):
        """
        Modifies the internal state based a change to the content and returns
        the sets of words added and removed.

        :Parameters:
            text : str
                The text content of a revision
            revision : `mixed`
                Revision meta data
            checksum : str
                A checksum hash of the text content (will be generated if not provided)

        :Returns:
            Three :class:`~mw.lib.persistence.Tokens` lists

            current_tokens : :class:`~mw.lib.persistence.Tokens`
                A sequence of :class:`~mw.lib.persistence.Token` for the
                processed revision
            tokens_added : :class:`~mw.lib.persistence.Tokens`
                A set of tokens that were inserted by the processed revision
            tokens_removed : :class:`~mw.lib.persistence.Tokens`
                A sequence of :class:`~mw.lib.persistence.Token` removed by the
                processed revision

        """
        if checksum is None:
            checksum = sha1(bytes(text, 'utf8')).hexdigest()

        version = Version()

        revert = self.revert_detector.process(checksum, version)
        if revert is not None:  # Revert

            # Empty words.
            tokens_added = Tokens()
            tokens_removed = Tokens()

            # Extract reverted_to revision
            _, _, reverted_to = revert
            version.tokens = reverted_to.tokens

        else:

            if self.last is None:  # First version of the page!

                version.tokens = Tokens(Token(t) for t in self.tokenize(text))
                tokens_added = version.tokens
                tokens_removed = Tokens()

            else:

                # NOTICE: HEAVY COMPUTATION HERE!!!
                #
                # OK.  It's not that heavy.  It's just performing a diff,
                # but you're still going to spend most of your time here.
                # Diffs usually run in O(n^2) -- O(n^3) time and most tokenizers
                # produce a lot of tokens.
                version.tokens, tokens_added, tokens_removed = \
                    self.last.tokens.compare(self.tokenize(text), self.diff)

        version.tokens.persist(revision)

        self.last = version

        return version.tokens, tokens_added, tokens_removed
