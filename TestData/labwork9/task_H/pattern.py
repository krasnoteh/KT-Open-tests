import random

def test_pattern(t, test_size, maximal_value):
    n_ = random.randint(2, test_size)
    m_ = random.randint(0, test_size)
    t.add_int(n_)
    t.add_int(m_)
    t.enter()

    # Generate n lines with four-character words
    words = [''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(4)) for _ in range(n_)]
    for word in words:
        t.add_string(word)
        t.enter()

    # Generate m lines with pairs of related words
    for _ in range(m_):
        word_pair = random.sample(words, 2)
        t.add_string(word_pair[0])
        t.add_string(word_pair[1])
        t.enter()