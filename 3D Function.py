import csv
import numpy as np
from multiprocessing import Pool

class DataEntry:
    def __init__(self, ID, phase, position, orientation):
        self.ID = int(ID)
        self.phase = float(phase)
        self.position = [float(position['x']), float(position['y']), float(position['z'])]
        self.orientation = [float(orientation['x']), float(orientation['y']), float(orientation['z'])]

def read_csv(filename):
    data = []
    with open(filename, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            entry = DataEntry(
                row['ID'],
                row['Phase'],
                {'x': row['Position_x'], 'y': row['Position_y'], 'z': row['Position_z']},
                {'x': row['Orientation_x'], 'y': row['Orientation_y'], 'z': row['Orientation_z']}
            )
            data.append(entry)
    return data

def generate_grid(window, resolution):
    z = np.linspace(-window, window, resolution)
    X, Y, Z = np.mgrid[-window:window:complex(resolution), -window:window:complex(resolution), -window:window:complex(resolution)]
    return X, Y, Z

def process_grid_chunk(args):
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
                    D_f = np.sinc((2 * np.pi / 8.3) * 4.5 * np.sin(theta))
                    partial_result[i, j, k] += (D_f / d) * np.exp(1j * (entry.phase + d * (2 * np.pi / 8.3)))
    return partial_result

def process_3d_array(X, Y, Z, XDCRs, resolution, num_processes):
    chunk_size = resolution // num_processes
    grid_chunks = [(X[i*chunk_size:(i+1)*chunk_size, :, :], Y[i*chunk_size:(i+1)*chunk_size, :, :], Z[i*chunk_size:(i+1)*chunk_size, :, :], XDCRs) for i in range(num_processes)]
    with Pool(processes=num_processes) as pool:
        results = list(pool.imap(process_grid_chunk, grid_chunks))
    result = np.concatenate(results, axis=0)
    return result

def calculate_magnitude_phase(result, resolution):
    result_magnitude = np.zeros((resolution, resolution, resolution), dtype=float)
    result_phase = np.zeros((resolution, resolution, resolution), dtype=float)
    for i in range(resolution):
        for j in range(resolution):
            for k in range(resolution):
                result_magnitude[i, k, j] = np.abs(result[i, j, k])
                result_phase[i, j, k] = np.angle(result[i, j, k])
    return result_magnitude, result_phase

def export_results_to_csv(results, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['X', 'Y', 'Z', 'Magnitude', 'Phase'])
        for i in range(results['magnitude'].shape[0]):
            for j in range(results['magnitude'].shape[1]):
                for k in range(results['magnitude'].shape[2]):
                    writer.writerow([
                        results['X'][i, j, k],
                        results['Y'][i, j, k],
                        results['Z'][i, j, k],
                        results['magnitude'][i, j, k],
                        results['phase'][i, j, k]
                    ])
        
def main():
    file_name = 'XDCRs.csv'
    XDCRs = read_csv(file_name)

    while True:
        try:
            num_processes = int(input("Enter Number of Processes: "))
            window = int(input("Enter window: "))
            resolution = int(input("Enter resolution: "))
            if resolution % num_processes != 0:
                print(f"Resolution must be a multiple of {num_processes}.")
                continue
            break
        except ValueError: 
            print("Please enter an integer")

    X, Y, Z = generate_grid(window, resolution)
    result = process_3d_array(X, Y, Z, XDCRs, resolution, num_processes)
    result_magnitude, result_phase = calculate_magnitude_phase(result, resolution)
    results = {'X': X, 'Y': Y, 'Z': Z, 'magnitude': result_magnitude, 'phase': result_phase}
    output_csv_filename = 'resultsLarge.csv'
    export_results_to_csv(results, output_csv_filename)
    print("Task Completed Successfuly")
if __name__ == "__main__":
    main()
