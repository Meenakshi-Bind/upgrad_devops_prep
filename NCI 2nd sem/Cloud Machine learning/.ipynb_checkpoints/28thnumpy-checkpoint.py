import numpy as np
import time
startPython = int(round(time.time() * 1000))
# Creates a list c by adding the elements of a and b
a = list(range(10000000))
b = list(range(10000000))
c = []
#This code can take up to 5 seconds to run depending on the type of machine you're using
for i in range(len(a)):
c.append(a[i] + b[i])
stopPython = int(round(time.time() * 1000))
# Below code does exactly the same thing but with Numpy Arrays
a = np.arange(10000000, dtype=int)
b = np.arange(10000000, dtype=int) # The Numpy code by comparison is shorter, doesn’t nee
d a loop and it is almost instantaneous by comparison
c = a + b
stopNumPy = int(round(time.time() * 1000))
# Here we express the time take by NumPy as a frac tion of the time taken by Python to pe
rform the same operation
print ((stopNumPy- stopPython)/(stopPython-startPython))
1. Array can be accessed using the square bracket notati