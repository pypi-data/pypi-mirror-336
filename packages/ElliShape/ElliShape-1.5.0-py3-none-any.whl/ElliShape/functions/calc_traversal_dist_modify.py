import numpy as np

def calc_traversal_dist_modify(ai):
    x_ = 0
    y_ = 0
    m = ai.shape[0]
    p = np.zeros((m, 2))  # Initialize position array
    dp = np.zeros((m, 2))  # Initialize displacement array

    for i in range(m):
        dx_ = np.sign(6 - ai[i]) * np.sign(2 - ai[i])
        dy_ = np.sign(4 - ai[i]) * np.sign(ai[i])
        x_ += dx_
        y_ += dy_
        p[i, 0] = x_
        p[i, 1] = y_
        dp[i, 0] = dx_
        dp[i, 1] = dy_

    return p, dp