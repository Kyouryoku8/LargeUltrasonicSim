# file_operations.py

import csv
from data_entry import DataEntry

def read_csv(filename):
    """
    Reads data from a CSV file and creates DataEntry objects.
    """
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

def export_results_to_csv(results, filename):
    """
    Exports processed results to a CSV file.
    """
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
