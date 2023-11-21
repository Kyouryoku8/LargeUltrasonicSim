import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define cube dimensions (extents of mesh grid)
mg_width = 0.28
mg_depth = 0.28
mg_height = 0.28
mg_height = 0.001
mesh_grid_cylinder = True
spacing = 0.001

# Create a mesh grid with 0.001 spacing within the cube
x = np.arange(-mg_width/2, mg_width/2, spacing)
y = np.arange(-mg_depth/2, mg_depth/2, spacing)
z = np.arange(-mg_height/2, mg_height/2, spacing)

xx, yy, zz = np.meshgrid(x, y, z)

if mesh_grid_cylinder:
  # Create a mask for points outside of a cylinder with a radius of 0.14
  # This will exclude points we don't care about.
  cylinder_radius = 0.14
  distance_from_center = np.sqrt(xx**2 + yy**2)  # Calculate distance from the center in x-y plane
  
  # Set points outside the cylinder to NaN
  xx[distance_from_center > cylinder_radius] = np.nan
  yy[distance_from_center > cylinder_radius] = np.nan
  zz[distance_from_center > cylinder_radius] = np.nan
