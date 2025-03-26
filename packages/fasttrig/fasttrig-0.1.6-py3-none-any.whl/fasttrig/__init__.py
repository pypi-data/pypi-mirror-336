from .sin import sin, cos, tan
try:
    from numba import njit
except ImportError:
    import warnings
    warnings.warn(
        "fasttrig: Numba is not installed. Performance will be significantly slower.",
        RuntimeWarning
    )