import random

def test_pattern(t, test_size, maximal_value):
    N = random.randint(1, test_size)
    k = random.randint(0, N)
    t.add_int(N)
    t.add_int(k)
    t.enter()

    for _ in range(N):
        n = random.randint(1, test_size)
        m = random.randint(0, test_size)
        t.add_int(n)
        t.add_int(m)
        t.enter()

        for _ in range(m):
            u = random.randint(1, n)
            v = random.randint(1, n)
            h = random.randint(-maximal_value, maximal_value)
            t.add_int(u)
            t.add_int(v)
            t.add_int(h)
            t.enter()