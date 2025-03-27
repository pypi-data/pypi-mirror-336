import numpy as np
from calc_traversal_dist_modify import calc_traversal_dist_modify
from calc_traversal_time_modify import calc_traversal_time_modify

def fast_calc_harmonic_coefficients_modify(ai, n, mode):
    """
    This function calculates the n-th set of four harmonic coefficients.
    The output is [an, bn, cn, dn].
    """
    if mode == 0:
        k = ai.shape[0]
        d,_ = calc_traversal_dist_modify(ai)
        # print(d)
        edist = d[-1, 0] ** 2 + d[-1, 1] ** 2
        if edist > 2:
            print("Error: Chain code is not closed.")
            return None
        elif edist > 0:
            vect = [-d[-1, 0], -d[-1, 1]]
            if vect[0] == 1 and vect[1] == 0:
                ai = np.append(ai, 0)
            elif vect[0] == 1 and vect[1] == 1:
                ai = np.append(ai, 1)
            elif vect[0] == 0 and vect[1] == 1:
                ai = np.append(ai, 2)
            elif vect[0] == -1 and vect[1] == 1:
                ai = np.append(ai, 3)
            elif vect[0] == -1 and vect[1] == 0:
                ai = np.append(ai, 4)
            elif vect[0] == -1 and vect[1] == -1:
                ai = np.append(ai, 5)
            elif vect[0] == 0 and vect[1] == -1:
                ai = np.append(ai, 6)
            elif vect[0] == 1 and vect[1] == -1:
                ai = np.append(ai, 7)

    # Maximum length of chain code
    k = ai.shape[0]

    # Traversal time
    t, dt = calc_traversal_time_modify(ai)

    # Traversal distance
    _, dd = calc_traversal_dist_modify(ai)

    # Basic period of the chain code
    T = t[-1]

    # Store this value to make computation faster
    two_n_pi = 2 * n * np.pi

    # Compute harmonic coefficients: an, bn, cn, dn
    delta_x = dd[0, 0]
    delta_y = dd[0, 1]
    delta_t = dt[0]
    q_x = delta_x / delta_t
    q_y = delta_y / delta_t
    cosp = np.cos(two_n_pi * t[0] / T)
    sinp = np.sin(two_n_pi * t[0] / T)
    sigma_a = q_x * (cosp - 1)
    sigma_b = q_x * sinp
    sigma_c = q_y * (cosp - 1)
    sigma_d = q_y * sinp

    for p in range(1, k):
        delta_x = dd[p, 0]
        delta_y = dd[p, 1]
        delta_t = dt[p]
        q_x = delta_x / delta_t
        q_y = delta_y / delta_t
        cost = np.cos(two_n_pi * t[p] / T)
        sint = np.sin(two_n_pi * t[p] / T)

        sigma_a += q_x * (cost - cosp)
        sigma_b += q_x * (sint - sinp)
        sigma_c += q_y * (cost - cosp)
        sigma_d += q_y * (sint - sinp)

        cosp = cost
        sinp = sint

    r = T / (2 * n ** 2 * np.pi ** 2)
    # print(r)
    a = r * sigma_a
    b = r * sigma_b
    c = r * sigma_c
    d = r * sigma_d

    # Assign to output
    # output = np.array([a, b, c, d])
    return [a, b, c, d]