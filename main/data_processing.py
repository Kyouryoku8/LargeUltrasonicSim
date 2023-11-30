# data_processing.py

import numpy as np
from multiprocessing import Pool

def generate_grid(window, resolution):
  """
  Generates 3D grid of points within a given window and resolution
  """
  X, Y, Z = np.mgrid[-window:window:complex(resolution), -window:window:complex(resolution), -window:window:complex(resolution)]
  return X, Y, Z

def process_grid_chunk(args):
  """
  Processes a chunk of the 3D grid
  """
  X_chunk, Y_chunk, Z_chunk, XDCRs = args
  partial_result = np.zeros_like(X_chunk, dtype=complex)
  for i in range(X_chunk.shape[0]):
    for j in range(Y_chunk.shape[1]):
      for k in range(Z_chunk.shape[2]):
        for entry in XDCRs:
          A = np.array([X_chunk[i, j, k] - entry.position[0], Y_chunk[i, j, k] - entry.position[1], Z_chunk[i, j, k] - entry.position[2]])
          B = np.array([entry.orientation[0], entry.orientation[1], entry.orientation[2]])
          dot_product = np.dot(A, B)
          magnitude_A = np.linalg.norm(A)
          magnitude_B = np.linalg.norm(B)
          cos_theta = dot_product / (magnitude_A * magnitude_B) if magnitude_A * magnitude_B != 0 else 0
          d = max(np.linalg.norm(A), 0.00001)
          theta = np.arccos(np.clip(cos_theta, -1, 1))
          D_f = np.sinc((2*np.pi / 8.3) * 4.5 * np.sin(theta))
          partial_result[i, j, k] += (D_f / d) * np.exp(1j * (entry.phase + d * (2 * np.pi / 8.3)))
  return partial_result

def process_3d_array(X, Y, Z, XDCRs, resolution, num_processes):
    """
    Divides the 3D grid into chunks and processes each chunk in parallel.
    """
    chunk_size = resolution // num_processes
    grid_chunks = [(X[i*chunk_size:(i+1)*chunk_size, :, :], Y[i*chunk_size:(i+1)*chunk_size, :, :], Z[i*chunk_size:(i+1)*chunk_size, :, :], XDCRs) for i in range(num_processes)]
    with Pool(processes=num_processes) as pool:
        results = list(pool.imap(process_grid_chunk, grid_chunks))
    result = np.concatenate(results, axis=0)
    return result

def calculate_magnitude_phase(result, resolution):
    """
    Calculates the magnitude and phase of the complex-valued result array.
    """
    result_magnitude = np.zeros((resolution, resolution, resolution), dtype=float)
    result_phase = np.zeros((resolution, resolution, resolution), dtype=float)
    for i in range(resolution):
        for j in range(resolution):
            for k in range(resolution):
                result_magnitude[i, j, k] = np.abs(result[i, j, k])
                result_phase[i, j, k] = np.angle(result[i, j, k])
    return result_magnitude, result_phase
  
          
