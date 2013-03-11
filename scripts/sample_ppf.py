import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm

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

# Countour
# From http://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html#contour-plots
fig3 = plt.figure()
ax3 = fig3.gca(projection='3d')
ax3.plot_surface(X, Y, Z, rstride=12, cstride=12, alpha=0.1, cmap=cm.gray)
cset = ax3.contour(X, Y, Z, zdir='z', offset=0, linewidth=4, cmap=cm.coolwarm)
cset = ax3.contour(X, Y, Z, zdir='x', offset=0, linewidth=4, cmap=cm.coolwarm)
cset = ax3.contour(X, Y, Z, zdir='y', offset=0, linewidth=4, cmap=cm.coolwarm)


for ax in [ax1, ax2, ax3]:
    ax.set_xlabel('Capital Stock')
    ax.set_ylabel('Investmnet')
    ax.set_zlabel('Labor')
    ax.set_title('Example PPF')
    ax.view_init(elev=20, azim=20)

p = ax1.plot_wireframe(X, Y, Z, rstride=2, cstride=2)
plt.figure(1)
plt.savefig('../resources/example_ppf_wire.png', dpi=400)  # Up dpi for final

p2 = ax2.plot_surface(X, Y, Z, alpha=.1)
cset = ax2.contour(X, Y, Z, zdir='z', offset=0, cmap=plt.cm.Accent)
cset = ax2.contour(X, Y, Z, zdir='x', offset=0, cmap=plt.cm.Accent)
cset = ax2.contour(X, Y, Z, zdir='y', offset=0, cmap=plt.cm.Accent)

plt.figure(3)
plt.savefig('../resources/example_ppf_contour.png', dpi=400)
