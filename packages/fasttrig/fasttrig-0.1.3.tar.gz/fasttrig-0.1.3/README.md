# fasttrig
<<<<<<< HEAD
Fast approximation of sin, cos, tan using forth degree polynomials
=======

A fast and lightweight approximation of sin, cos, and tan using 4th-degree polynomials.

Accuracy: Error < 0.001


## Example

```python
from fasttrig import P1_fast, fast_cos, fast_tan
import numpy as np

print(P1_fast(np.pi/2))  
print(fast_cos(np.pi))   
print(fast_tan(np.pi/4)) 
```
>>>>>>> 08b946d (Initial commit: fasttrig first release)
