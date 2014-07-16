from nose.tools import eq_

from ..state import State


def test_state():
    contents_revisions = [
        ("Apples are red.", 0),
        ("Apples are blue.", 1),
        ("Apples are red.", 2),
        ("Apples are tasty and red.", 3),
        ("Apples are tasty and blue.", 4)
    ]

    state = State()

    token_sets = [state.process(c, r) for c, r in contents_revisions]

    for i, (content, revision) in enumerate(contents_revisions):
        eq_("".join(token_sets[i][0].texts()), content)

    eq_(token_sets[0][0][0].text, "Apples")
    eq_(len(token_sets[0][0][0].revisions), 5)
    eq_(token_sets[0][0][4].text, "red")
    eq_(len(token_sets[0][0][4].revisions), 3)
