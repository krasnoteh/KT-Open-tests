import random

def test_pattern(t, test_size, maximal_value):
    N_ = random.randint(1, test_size)
    M_ = random.randint(0, min(test_size, N_*(N_-1)//2))  # Ensure M is within valid range
    
    t.add_int(N_)
    t.add_int(M_)
    t.enter()

    for i_ in range(M_):
        x_ = random.randint(1, N_)
        y_ = random.randint(1, N_)
        l_ = random.randint(0, maximal_value)
        
        t.add_int(x_)
        t.add_int(y_)
        t.add_int(l_)
        t.enter()