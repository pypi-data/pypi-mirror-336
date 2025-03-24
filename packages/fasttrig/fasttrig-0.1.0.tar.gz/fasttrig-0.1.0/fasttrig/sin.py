
import numpy as np

def P1_fast(x):
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

def fast_cos(x):
    return P1_fast(x + np.pi / 2)

def fast_tan(x):
    cos_val = fast_cos(x)
    if abs(cos_val) < 1e-6:
        return float('inf') if P1_fast(x) > 0 else float('-inf')
    return P1_fast(x) / cos_val
