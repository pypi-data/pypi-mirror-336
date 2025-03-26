# fasttrig

Requires Numba for optimal performance.

A fast and lightweight approximation of sin, cos, and tan using 4th-degree polynomials.

Unit: radian

Accuracy: Error < 0.001

Important: Numba is required for fasttrig to achieve high performance.
Without Numba, performance will be even slower than NumPy.
With Numba, the efficiency can be 1.5 to 3.0 times NumPy.




## Example

```python
import fasttrig
import numpy as np


x = np.linspace(-np.pi, np.pi, 1000000)

y = fasttrig.sin(x)
c = fasttrig.cos(x)
t = fasttrig.tan(x)
#Scalar
z = fasttrig.sin(1902.0808)



