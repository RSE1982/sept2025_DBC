'''
Author: Robert Elliott
Date: 2025-09-23 12:00:00
Description: Example code for DataCoach Session on 2025-09-23
'''
import os
import numpy as np

os.system("clear")

# # 20250923.py

# arr = np.array([[1, 2, 3, 4],[5, 6, 7, 8]])


# print(arr[1, 1:3])



# A = 0.3

# print(A)
# print(type(A))

# rolls = np.random.randint(1, 7, size=1000000)
# counts = np.bincount(rolls)[1:]
# faces = np.arange(1, 7)

# print(f"Dice face counts: {counts}")

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# plt.bar(faces, counts)
# plt.xlabel('Dice Face')
# plt.ylabel('Counts')
# plt.title('Dice Roll Simulation')
# plt.show()

x = np.linspace(0, 500, 500)
y = np.linspace(0, 500, 500)
X,Y = np.meshgrid(x, y)
Z = np.sin(X) * np.cos(Y)

contour = plt.contour(X, Y, Z, levels=50, cmap='viridis')
plt.colorbar(contour)
plt.title('Contour Plot of Z = sin(X) * cos(Y)')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.show()
