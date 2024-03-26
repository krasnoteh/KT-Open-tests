import random

def test_pattern(t, test_size, maximal_value):
    n_ = random.randint(1, test_size)
    m_ = random.randint(1, test_size)
    q_ = random.randint(1, test_size)
    t.add_int(n_)
    t.add_int(m_)
    t.add_int(q_)
    t.enter()
    for i_ in range(m_):
        t.add_int(random.randint(0, n_))
        t.add_int(random.randint(0, n_))
        t.enter()
    for i_ in range(q_):
        t.add_int(random.randint(0, n_))
        t.add_int(random.randint(0, n_))
        t.enter()
