import numpy as np

def calc_traversal_time_modify(ai):
    t_ = 0
    m = ai.shape[0]
    t = np.zeros(m)
    dt = np.zeros(m)

    for i in range(m):
        dt_ = 1 + ((np.sqrt(2) - 1) / 2) * (1 - (-1) ** ai[i])
        t_ += dt_
        t[i] = t_
        dt[i] = dt_
    return t, dt