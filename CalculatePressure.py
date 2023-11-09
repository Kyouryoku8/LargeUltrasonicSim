# Calculate pressure at each point
# This is currently 2D and needs to become 3D
result = np.zeros((resolution, resolution), dtype=complex)
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
