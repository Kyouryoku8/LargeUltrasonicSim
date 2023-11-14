pip install pandas openpyxl

# Function for creating transducers in x, y, and z dimension (3D)
def add_xdcr_record(id, phase, pos_x, pos_y, pos_z, ori_x, ori_y, ori_z):
  record = {
    'ID' : id,
    'Phase' : phase, 
    'PosX': pos_x, 
    'PosY': pos_y, 
    'PosZ': pos_z, 
    'OriX': ori_x, 
    'OriY': ori_y, 
    'OriZ': ori_z
  }
  xdcr_records.append(record)

# User defined variables
num_rings = 3 # number of rings in system
ring_spacing = 50 # Distance between rings 
XDCRs = 5 # Number of transducers per ring
window = 200 # Span of X, Y, Z coordinates
resolution = 100 # Resolution of display grid
r = 100 # Radius of rings


# Add transducer information
xdcr_recoreds = []
# Add transducer information
for ring in range(num_rings):
    z_position = ring * ring_spacing
    for i in range(XDCRs):
        add_xdcr_record(
            id=1,
            phase=(i / XDCRs * 2 * np.pi),
            pos_x=np.cos(i / XDCRs * 2 * np.pi) * r,
            pos_y=np.sin(i / XDCRs * 2 * np.pi) * r,
            pos_z=z_position,
            ori_x=-np.cos(i / XDCRs * 2 * np.pi),
            ori_y=-np.sin(i / XDCRs * 2 * np.pi),
            ori_z=0
        )

# Generate grid
z = np.linspace(-window, window, resolution)
X, Y, Z = np.mgrid[-window:window:complex(resolution), -window:window:complex(resolution), -window:window:complex(resolution)]

# Initialize 3D arrays for results
result = np.zeros((resolution, resolution, resolution), dtype=complex)
result_magnitude = np.zeros((resolution, resolution, resolution), dtype=float)
result_phase = np.zeros((resolution, resolution, resolution), dtype=float)

for i in range(resolution):
    for j in range(resolution):
        for k in range(resolution):
            for record in xdcr_records:
                # 3D position vector from the point to transducer
                A = np.array([X[i, j, k] - record['PosX'], Y[i, j, k] - record['PosY'], Z[i, j, k] - record['PosZ']])
                # 3D orientation vector of transducer
                B = np.array([record['OriX'], record['OriY'], record['OriZ']])
                dot_product = np.dot(A, B)
                # Magnitudes of A, B
                magnitude_A = np.linalg.norm(A)
                magnitude_B = np.linalg.norm(B)
                cos_theta = dot_product / (magnitude_A * magnitude_B) # Cosine of the angle between A and B
                d = max(np.linalg.norm(A), 0.00001)  # Distance with a minimum value to avoid division by zero
                theta = np.arccos(cos_theta) # Calculate angle in radians
                D_f = np.sinc((2 * np.pi / 8.3) * 4.5 * np.sin(theta)) # Calculate the pattern from the XDCR (assuming this remains valid in 3D)
                result[i, j, k] += (D_f / d) * np.exp(1j * (record['Phase'] + d * (2 * np.pi / 8.3)))  # Calculate the value for each point

# Extract magnitude and phase for visualization or storage
for i in range(resolution):
    for j in range(resolution):
        for k in range(resolution):
            result_magnitude[i, j, k] = np.abs(result[i, j, k])
            result_phase[i, j, k] = np.angle(result[i, j, k])




      
