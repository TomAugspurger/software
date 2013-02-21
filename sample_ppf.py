import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D

# Sphere at origin: x^2 + y^2 + z*2 = r*2

x = np.linspace(0, 2, 50)
y = np.linspace(0, 2, 50)

x_ = np.outer(np.cos(x), np.sin(y))
y_ = np.outer(np.sin(x), np.sin(y))
z_ = np.outer(np.ones(np.size(x)), np.cos(y))

fig = plt.figure()
ax = Axes3D(fig)
ax.plot_wireframe(x_, y_, z_)

# Method 2
X, Y = np.meshgrid(x, y)
Z = np.sqrt(4 - X ** 2 - Y ** 2)

fig1 = plt.figure()
ax1 = fig1.add_subplot(1, 1, 1, projection='3d')

p = ax1.plot_wireframe(X, Y, Z)
