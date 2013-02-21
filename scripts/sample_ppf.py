import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D

# TODO: Program in the viewing angle.
# Sphere at origin: x^2 + y^2 + z*2 = r*2

x = np.linspace(0, 2, 100)
y = np.linspace(0, 2, 100)

x_ = np.outer(np.cos(x), np.sin(y))
y_ = np.outer(np.sin(x), np.sin(y))
z_ = np.outer(np.ones(np.size(x)), np.cos(y))

fig = plt.figure()
ax = Axes3D(fig)
ax.plot_wireframe(x_, y_, z_)

# Method 2
X, Y = np.meshgrid(x, y)
Z = np.sqrt(4 - X ** 2 - Y ** 2)
Z[np.isnan(Z)] = 0

# Wireframe
fig1 = plt.figure()
ax1 = fig1.add_subplot(1, 1, 1, projection='3d')

ax1.set_xlabel('Capital Stock')
ax1.set_ylabel('Investmnet')
ax1.set_zlabel('Labor')
ax1.set_title('Example PPF')
p = ax1.plot_wireframe(X, Y, Z, rstride=2, cstride=2)
# Adjust view
plt.savefig('../resources/example_ppf_wire.png', dpi=100)  # Up dpi for final

# Surface
fig2 = plt.figure()
ax2 = fig2.add_subplot(1, 1, 1, projection='3d')

ax2.set_title('Example PPF')
ax2.set_xlabel('Capital Stock')
ax2.set_ylabel('Investmnet')
ax2.set_zlabel('Labor')
p2 = ax2.plot_surface(X, Y, Z, cmap=plt.cm.jet)
# Adjust view
plt.savefig('../resources/example_ppf_surface.png', dpi=100)
