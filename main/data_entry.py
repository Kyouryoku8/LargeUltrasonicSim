# data_entry.py

class DataEntry:
    """
    Represents a single data entry with ID, phase, position, and orientation.
    """

    def __init__(self, ID, phase, position, orientation):
        """
        Initializes a new instance of DataEntry.

        :param ID: The identifier for the data entry.
        :param phase: The phase associated with the data entry.
        :param position: A dictionary containing the 'x', 'y', and 'z' positions.
        :param orientation: A dictionary containing the 'x', 'y', and 'z' orientation.
        """
        self.ID = int(ID)
        self.phase = float(phase)
        self.position = [float(position['x']), float(position['y']), float(position['z'])]
        self.orientation = [float(orientation['x']), float(orientation['y']), float(orientation['z'])]

