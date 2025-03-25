# fasttrig



A fast and lightweight approximation of sin, cos, and tan using 4th-degree polynomials.

Unit: radian

Accuracy: Error < 0.001




## Example

```python
import numpy as np
from fasttrig import P1_fast, fast_cos, fast_tan

print(P1_fast(np.pi))         
print(P1_fast([0, np.pi/2, np.pi])) 
print(fast_cos([0, np.pi/2, np.pi]))
print(fast_tan(np.linspace(0, 2*np.pi, 100)))

```




