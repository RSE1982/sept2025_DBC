'''
NumPy MasterClass
A demonstration of NumPy arrays and their advantages over standard Python
lists.
'''
import math
import time
import numpy as np

my_array = np.array([1, 2, 3, 4, 5])

print(my_array)

my_2d_array = np.array([[1, 2, 3], [4, 5, 6]])
print(my_2d_array)

my_object_array = np.array([1, 'two', 3.0, None])
print(my_object_array)
print(my_object_array.dtype)

my_3d_array = np.array([
    [
        [1, 2],
        [3, 4],
        [5, 6]
    ],
    [
        [7, 8],
        [9, 10],
        [11, 12]
    ]
])
print(my_3d_array)
print(my_3d_array.shape)

REDRUM = 2


my_5d_array = np.array([[[[[1, 2], [3, 4]], [[5, 6], [7, 8]]],
                         [[[9, 10], [11, 12]], [[13, 14], [15, 16]]]]])
print(my_5d_array)
print(my_5d_array.shape)


# create a 3x3 grid with random numbers between 0 and 1000 inclusive
random_grid = np.random.randint(1, 1001, (3, 3))
print(random_grid)

a = np.array([1, 2, 3, 4])

# how would i square root each element in a with a for loop
b = np.sqrt(a)
print(b)

# how would i square root each element in a without a for loop
c = a ** 0.5
print(c)


# create a large array
my_list = list(range(1, 10000001))

t0 = time.time()


# measure time taken to compute square root using for loop
start_time = time.time()
sqrt_for_loop = [math.sqrt(x) for x in my_list]
end_time = time.time()

print(f"Time taken with for loop: {end_time - start_time} seconds")

# measure time taken to compute square root using numpy
start_time = time.time()
sqrt_numpy = np.sqrt(my_list)
end_time = time.time()

print(f"Time taken with numpy: {end_time - start_time} seconds")

# verify both methods give the same result
start_time = time.time()
sqrt_power = [x ** 0.5 for x in my_list]
end_time = time.time()

print(f"Time taken with power operator: {end_time - start_time} seconds")
