import random

def test_pattern(t, test_size, maximal_value):
    n_ = random.randint(1, test_size)
    m_ = random.randint(1, test_size)
    k_ = random.randint(1, test_size)
    t.add_int(n_)
    t.add_int(m_)
    t.add_int(k_)
    t.enter()
    for i_ in range(m_):
        t.add_int(random.randint(1, n_))
        t.add_int(random.randint(1, n_))
        t.add_int(random.randint(1, maximal_value))
        t.enter()
    for i_ in range(k_):
        t.add_int(random.randint(1, n_))
        t.add_int(random.randint(1, n_))
        t.add_int(random.randint(1, maximal_value))
        t.enter()
