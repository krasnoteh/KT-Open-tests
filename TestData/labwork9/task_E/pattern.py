import random

def test_pattern(t, test_size, maximal_value):
    n_ = random.randint(1, test_size)
    m_ = random.randint(0, min(test_size, 10**5))
    t.add_int(n_)
    t.add_int(m_)
    t.enter()
    for i_ in range(m_):
        x_ = random.randint(1, n_)
        y_ = random.randint(1, n_)
        t.add_int(x_)
        t.add_int(y_)
        t.enter()