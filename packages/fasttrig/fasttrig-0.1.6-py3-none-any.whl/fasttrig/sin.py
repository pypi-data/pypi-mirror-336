
import numpy as np
from numba import njit, prange

def _P1_fast_scalar(x):
    x = x % (2 * np.pi)

    def O1(x):
        deg = 180 * x / np.pi
        part1 = (deg * (180 - deg)) / 8100
        part2 = (
            -0.0368163 * (x - 1.5707963048036) ** 4
            + 0.09084058 * (x - 1.5707963048036) ** 2
        )
        return part1 - part2

    if x <= np.pi:
        return O1(x)
    else:
        return -O1(2 * np.pi - x)

@njit(parallel=True, fastmath=True)
def _P1_fast_vec(x):
    out = np.empty_like(x)
    for i in prange(x.shape[0]):
        xi = x[i] % (2 * np.pi)

        if xi <= np.pi:
            deg = 180 * xi / np.pi
            part1 = (deg * (180 - deg)) / 8100
            part2 = (
                -0.0368163 * (xi - 1.5707963048036) ** 4
                + 0.09084058 * (xi - 1.5707963048036) ** 2
            )
            out[i] = part1 - part2
        else:
            xj = 2 * np.pi - xi
            deg = 180 * xj / np.pi
            part1 = (deg * (180 - deg)) / 8100
            part2 = (
                -0.0368163 * (xj - 1.5707963048036) ** 4
                + 0.09084058 * (xj - 1.5707963048036) ** 2
            )
            out[i] = -(part1 - part2)
    return out

def sin(x):
    if np.isscalar(x):
        return _P1_fast_scalar(x)
    else:
        x = np.asarray(x, dtype=np.float64)
        return _P1_fast_vec(x)

def cos(x):
    if np.isscalar(x):
        return sin(x + np.pi / 2)
    else:
        x = np.asarray(x, dtype=np.float64)
        return sin(x + np.pi / 2)

def tan(x):
    s = sin(x)
    c = cos(x)
    if np.isscalar(x):
        if abs(c) < 1e-6:
            return float('inf') if s > 0 else float('-inf')
        return s / c
    else:
        c = np.where(np.abs(c) < 1e-6, np.nan, c)
        return s / c
