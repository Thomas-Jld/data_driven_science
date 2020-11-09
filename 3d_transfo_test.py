from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import numpy as np
import matplotlib.pyplot as plt 


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_title("3D transformations")

transformations = ["Original", "X scaling", "75° rotation", "Z Translation"]
colors = ["#e66101", "#fdb863", "#b2abd2", "#5e3c99"]
alpha = "d0"

"""
Drawing the original
"""
points = np.array([
    [1, 1, 0],
    [3, 4, 0],
    [4, 4, 0],
    [3, 1, 0]
    ])


ax.set_xlim(0,9)
ax.set_ylim(-8,8)
ax.set_zlim(0,4)

ax.scatter(points[:,0], points[:, 1], points[:, 2], s= 50,c=colors[0], label = transformations[0])

vertexes = [points]
poly = Poly3DCollection(vertexes)
poly.set_color(colors[0] + alpha)
poly.set_edgecolor(colors[0])
ax.add_collection3d(poly)

"""
Scaling x2 on X axis
"""
m_scaling = np.array([
    [2, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
    ])

points1 = points @ m_scaling

ax.scatter(points1[:,0], points1[:, 1], points1[:, 2], s= 50, c = colors[1], label = transformations[1])

vertexes = [points1]
poly1 = Poly3DCollection(vertexes)
poly1.set_color(colors[1] + alpha)
poly1.set_edgecolor(colors[1])
ax.add_collection3d(poly1)

"""
75° rotation on Z axis
"""
theta = np.pi*75/180

m_rotation = np.array([
    [np.cos(theta), -np.sin(theta), 0],
    [np.sin(theta), np.cos(theta), 0],
    [0            , 0            , 1]
])
points2 = points1 @ m_rotation

ax.scatter(points2[:,0], points2[:, 1], points2[:, 2],  s= 50, c= colors[2], label = transformations[2])

vertexes = [points2]
poly2 = Poly3DCollection(vertexes)
poly2.set_color(colors[2] + alpha)
poly2.set_edgecolor(colors[2])
ax.add_collection3d(poly2)

"""
+3 Translation on Z axis
"""
m_translation = np.array([0, 0, 3])

points3 = points2 + m_translation

ax.scatter(points3[:, 0], points3[:, 1], points3[:, 2],  s= 50, c= colors[3], label = transformations[3])

vertexes = [points3]
poly3 = Poly3DCollection(vertexes)
poly3.set_color(colors[3] + alpha)
poly3.set_edgecolor(colors[3])
ax.add_collection3d(poly3)


ax.locator_params(nbins=5)

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.legend()
plt.show()