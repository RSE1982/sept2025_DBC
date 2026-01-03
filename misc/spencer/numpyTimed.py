import numpy as np
import time
import math
import cupy as cp

# Create big data
N = 10_000_001
my_list = list(range(N))
arr = np.arange(N)

# Python loop version
t0 = time.perf_counter()
roots_list = [math.sqrt(num) for num in my_list]
t1 = time.perf_counter()

# NumPy version (vectorised)
roots_arr = np.sqrt(arr)
t2 = time.perf_counter()

print(f"Python list loop: {t1 - t0:.4f} seconds")
print(f"NumPy array vectorised loop: {t2 - t1:.4f} seconds")seconds")

