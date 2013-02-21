import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D

# Sphere at origin: x^2 + y^2 + z*2 = r*2

x = np.linspace(0, 2, 100)
y = np.linspace(0, 2, 100)

X, Y = np.meshgrid(x, y)
Z = np.sqrt(4 - X ** 2 - Y ** 2)
Z[np.isnan(Z)] = 0

# Wireframe
fig1 = plt.figure()
ax1 = fig1.add_subplot(1, 1, 1, projection='3d')


# Surface
fig2 = plt.figure()
ax2 = fig2.add_subplot(1, 1, 1, projection='3d')

for ax in [ax1, ax2]:
    ax.set_xlabel('Capital Stock')
    ax.set_ylabel('Investmnet')
    ax.set_zlabel('Labor')
    ax.set_title('Example PPF')
    ax.view_init(elev=14, azim=10)

p = ax1.plot_wireframe(X, Y, Z, rstride=2, cstride=2)
plt.figure(1)
plt.savefig('../resources/example_ppf_wire.png', dpi=100)  # Up dpi for final

p2 = ax2.plot_surface(X, Y, Z, cmap=plt.cm.jet)
plt.figure(2)
plt.savefig('../resources/example_ppf_surface.png', dpi=100)
