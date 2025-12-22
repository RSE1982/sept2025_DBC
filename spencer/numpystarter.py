my_list = [1, 2, 3]

import numpy as np
my_array = np.array([1, 2, 3])
print(type(my_list), type(my_array))

"""
What are the difference between a list and a numpy array?
Data Types: numpy is fixed and for numerical data though
object can be stored.
Memory: Numpy use less memory (more efficient)
Speed: Numpy is faster (C)
Operations: Numpy is math ready
Shape: Numpy is 'nd' is the box and can reshape fast
Ecosystem: numpoy is backbone for Pandas, scihit learn,
tensorFlow
"""

my_list = [1, 2, 3]
print(my_list * 2)

# output is [1, 2, 3, 1, 2, 3]

my_array = np.array([1, 2, 3])
print(my_array * 2)

# output is [2, 4, 6]

# How do you make a 3d array
arr3d = np.array([
    [[1, 2, 3, 4],
     [5, 6, 7, 8],
     [9, 10, 11, 12]],
    [[13, 14, 15, 16],
     [17, 18, 19, 20],
     [21, 22, 23, 24]]
    ])

print("Shape: ", arr3d.shape)
print("ND? ", arr3d.ndim)

a = list(range(1, 10, 2))
print(a)

b = np.arange(1, 10, 2)
print(b)

c = np.zeros((2, 3))
print(c)

d = np.random.randint(1, 1_000_000, (9, 9))
print(d)

# Create a grid of 3 x 3 of random int from 1 to a 1000 inclusive
ans = np.random.randint(1, 1_000, (3, 3))
print(ans)

# Array Operations
a = np.array([1, 2, 3, 4])
print(a * 2)  # vectorised
print(a + 10)  # broadcasting
print(np.sqrt(a))  # universal function

# How would this look if we did this in a python loop
my_list = [1, 2, 3, 4]
doubled = [num*2 for num in my_list]
print(doubled)
add10 = [num+10 for num in my_list]
print(add10)

import math
roots = [math.sqrt(num) for num in my_list]
print(roots)

