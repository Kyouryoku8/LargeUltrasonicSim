# Import libraries
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
# Function to add a new transducers (XDCRs)
def add_xdcr_record(id, phase, pos_x, pos_y, ori_x, ori_y):
    record = {
        'ID': id,
        'Phase': phase,
        'PosX': pos_x,
        'PosY': pos_y,
        'OriX': ori_x,
        'OriY': ori_y
    }
    xdcr_records.append(record)
    
    
# User Defined Variables
# XDCRs are arranged in a circle pointing inward.
# The number of XDCRs and the radius of the circle are defined below:
XDCRs = 2 # Number of transducers in a ring
r = 100 # Radius from the center of the plot to each XDCR
#Display settings:
window = 50 # Span of X and Y from -window to window
resolution = 100 # Resolution of display



# Generate the mesh grid
x = np.linspace(-window, window, resolution)
y = np.linspace(-window, window, resolution)
X, Y = np.meshgrid(x, y)
# Populate the transducer information
xdcr_records = []
for i in range(XDCRs):
    add_xdcr_record(1, (i/XDCRs*2*np.pi), np.cos(i/XDCRs*2*np.pi)*r,  np.sin(i/XDCRs*2*np.pi)*r, \
                                         -np.cos(i/XDCRs*2*np.pi),   -np.sin(i/XDCRs*2*np.pi))
# Calculate pressure at each point
result = np.zeros((resolution, resolution), dtype=complex)
result2 = np.zeros((resolution, resolution), dtype=float)
result3 = np.zeros((resolution, resolution), dtype=float)
for i in range(resolution):
    for j in range(resolution):
        for record in xdcr_records:
            # Calculate dot product of two vectors
            A = np.array([(x[i] - record['PosX']), (y[j]) - record['PosY']])
            B = np.array([record['OriX'], record['OriY']])
            dot_product = np.dot(A, B)
            # Calculate the magnitudes (lengths) of A and B
            magnitude_A = np.linalg.norm(A)
            magnitude_B = np.linalg.norm(B)
            # Calculate the cosine of the angle between A and B
            cos_theta = dot_product / (magnitude_A * magnitude_B)
            d = max(((record['PosX'] - x[i])**2 + (record['PosY'] - y[j])**2)**0.5,0.00001)
            # Calculate the angle in radians
            theta = np.arccos(cos_theta)
            # Calculate the pattern from the XDCR
            D_f = np.sinc((2*np.pi/8.3) * 4.5 * np.sin(theta))
            # Calculate the value for each point (for each transducer)
            result[j,i] += 1*1*(D_f/d) * np.exp(1j * (record['Phase']+d*(2*np.pi/8.3)))
            
# Remove complex component for display
for i in range(resolution):
    for j in range(resolution):
        result2[i,j] = np.abs(result[i,j])
# Remove complex component for display
for i in range(resolution):
    for j in range(resolution):
        result3[i,j] = np.angle(result[i,j])
        
# Plot the interferrence pattern
plt.imshow(result3, extent=[-window, window, -window, window], origin='lower', cmap='hsv')
plt.colorbar(label='Amplitude')
plt.title('Interference Pattern (Amplitude) XDCRs=' + str(XDCRs))
plt.xlabel('X')
plt.ylabel('Y')
plt.show()
