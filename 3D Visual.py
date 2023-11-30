# Simple 3D plot of position in 2D vs amplitude for XDCRs

import numpy as np
import matplotlib.pyplot as plt
from pandas import *

data = read_csv("resultsLarge.csv")

X = np.array(data['X'].tolist())
Y = np.array(data['Y'].tolist())
Z = np.array(data['Magnitude'].tolist())

ax = plt.axes(projection='3d')
ax.plot_trisurf(X, Y, Z, linewidth=0, edgecolor='none')

plt.title("XDCR Amplitude")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Amplitude")

plt.show()
