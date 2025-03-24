import numpy as np

try:
    from numba import vectorize, float64
    use_vectorized = True
except ImportError:
    use_vectorized = False


def _p1_core(x):
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


if use_vectorized:
    P1_fast = vectorize([float64(float64)], nopython=True)(_p1_core)
else:
    def P1_fast(x):
        x = np.asarray(x)
        if x.ndim == 0:
            return _p1_core(float(x))
        else:
            return np.fromiter((_p1_core(xi) for xi in x), dtype=np.float64, count=len(x))


def fast_cos(x):
    return P1_fast(np.asarray(x) + np.pi / 2)

def fast_tan(x):
    sin_val = P1_fast(x)
    cos_val = fast_cos(x)
    cos_val = np.where(np.abs(cos_val) < 1e-8, 1e-8, cos_val)
    return sin_val / cos_val

