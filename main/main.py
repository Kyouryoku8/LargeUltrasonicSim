# main.py

from data_entry import DataEntry
from file_operations import read_csv, export_results_to_csv
from data_processing import generate_grid, process_3d_array, calculate_magnitude_phase

def main():
    file_name = input("Enter the name of the .csv file containing XDCR data: ")

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
    output_csv_filename = input("Enter the desired output file name: "))
    export_results_to_csv(results, output_csv_filename)

    print("Task Completed Successfully")

if __name__ == "__main__":
    main()

