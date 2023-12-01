# file_operations.py

import csv
import shutil
from PyQt5.QtWidgets import QFileDialog
from data_entry import DataEntry

def read_csv(filename):
    """
    Reads data from a CSV file and creates DataEntry objects.
    Converts units from meters to millimeters.
    """
    data = []
    with open(filename, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            entry = DataEntry(
                row['ID'],
                row['Phase'],
                {'x': float(row['Position_x'])*1000, 'y': float(row['Position_y'])*1000, 'z': float(row['Position_z'])*1000},
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

def copy_files_to_folder(target_folder):
    # Open file dialog to select files
    files, _ = QFileDialog.getOpenFileNames(caption="Select files to import")
    
    # Copy selected files to the target folder
    for file_path in files:
        try:
            shutil.copy(file_path, target_folder)
        except Exception as e:
            print(f"Error copying file {file_path}: {e}")
