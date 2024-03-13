import random

def test_pattern(t, test_size, maximal_value):
    n_ = random.randint(1, test_size)
    q_ = random.randint(1, test_size)
    t.add_int(n_)
    t.add_int(q_)
    t.enter()
    for i_ in range(q_):
        command_ = random.randint(1, 2)
        t.add_int(command_)
        if (command_ == 1):
            a_ = random.randint(1, n_)
            b_ = random.randint(1, n_)
            t.add_int(a_)
            t.add_int(b_)
        if (command_ == 2):
            a_ = random.randint(1, n_)
            t.add_int(a_)
        t.enter()