from nose.tools import eq_

from .. import autovivifying


def test_word_count():
    words = """
    I am a little teapot short and stout.  Here is my handle and here is my
    spout.  The red fox jumps over the lazy brown dog.  She sells sea shells
    by the sea shore.
    """.replace(".", " ").split()

    # Lame way
    lame_counts = {}
    for word in words:
        if word not in lame_counts:
            lame_counts[word] = 0

        lame_counts[word] += 1

    # Awesome way
    awesome_counts = autovivifying.Dict(  # Autovivifies entries with zero.
                                          vivifier=lambda k: 0  # Useful for counting.
    )
    for word in words:
        awesome_counts[word] += 1

    eq_(lame_counts, awesome_counts)
