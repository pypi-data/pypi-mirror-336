import numpy as np

try:
    from numba import jit
    use_jit = True
except ImportError:
    use_jit = False

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

if use_jit:
    _P1_fast_scalar = jit(_P1_fast_scalar, nopython=True)

def P1_fast(x):
    x = np.asarray(x)

    if x.ndim == 0:
        return _P1_fast_scalar(float(x))  
    else:
        return np.fromiter((_P1_fast_scalar(xi) for xi in x), dtype=np.float64, count=len(x))

def fast_cos(x):
    return P1_fast(np.asarray(x) + np.pi / 2)

def fast_tan(x):
    sin_val = P1_fast(x)
    cos_val = fast_cos(x)
    cos_val = np.where(np.abs(cos_val) < 1e-8, 1e-8, cos_val)
    return sin_val / cos_val
