#!/usr/bin/python3

import numpy as np

# from ellishape_cli.global_vars import log


def get_curve_from_efd(a, b, c, d, n_order: int, n_dots: int, A0=0, C0=0):
    """
    Convert efd coefficients to dots of curve
    Args:
        a, b, c, d: [n_order*1] array
        n_order: how many order of coefficients to use
        A0:
        C0:
    Returns:
        dots: [n_dots*2] matrix
    """
    # log.debug(f'{A0=} {C0=}')
    # log.debug([a[0], b[0], c[0], d[0]])
    assert a.shape[0] == b.shape[0] == c.shape[0] == d.shape[0]
    total_order = a.shape[0]
    # similar to ShyBoy233's
    a = np.reshape(a, (total_order, 1))
    b = np.reshape(b, (total_order, 1))
    c = np.reshape(c, (total_order, 1))
    d = np.reshape(d, (total_order, 1))
    print("a:", a[:5])  # 检查前5个a系数
    print("b:", b[:5])  # 检查前5个b系数
    print("c:", c[:5])  # 检查前5个c系数
    print("d:", d[:5])  # 检查前5个d系数
    # log.debug([a[0], b[0], c[0], d[0]])
    t = np.linspace(0, 1.0, num=n_dots, endpoint=False)
    n = np.arange(1, n_order + 1).reshape((-1, 1))
    x_t = A0 + np.sum(
        a[:n_order] * np.cos(2 * n * np.pi * t) +
        b[:n_order] * np.sin(2 * n * np.pi * t),
        axis=0)
    y_t = C0 + np.sum(
        c[:n_order] * np.cos(2 * n * np.pi * t) +
        d[:n_order] * np.sin(2 * n * np.pi * t),
        axis=0)
    # log.debug(f'{x_t[0]=} {y_t[0]=}')
    dots = np.concatenate([x_t.reshape(-1, 1), y_t.reshape(-1, 1)], axis=1)
    return dots
