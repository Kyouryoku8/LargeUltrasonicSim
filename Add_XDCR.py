import csv

# Define a class to store each row of the CSV as an object
class DataEntry:
    def __init__(self, ID, phase, position, orientation):
        self.ID = int(ID)
        self.phase = float(phase)
        self.position = [float(position['x']), float(position['y']), float(position['z'])]
        self.orientation = [float(orientation['x']), float(orientation['y']), float(orientation['z'])]

# Function to read the CSV file and store data in a structured variable array
def read_csv(filename):
    data = []
    with open(filename, newline='') as csvfile:
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

# Read data from XDCRs.csv into the variable XDCRs
file_name = 'XDCRs.csv'
XDCRs = read_csv(file_name)

# Print data to screen (not needed anymore)
#for entry in XDCRs:
#    print(f"ID: {entry.ID}, Phase: {entry.phase}, Position: {entry.position}, Orientation: {entry.orientation}")
