# calculation_dialog.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QApplication, QPushButton, QLineEdit, QLabel, QWidget, QTextEdit
from data_entry import DataEntry
from file_operations import read_csv, export_results_to_csv
from data_processing import generate_grid, process_3d_array, calculate_magnitude_phase
import os

class CalculationDialog(QDialog):
    def __init__(self, filePath, parent=None):
        super().__init__(parent)
        self.filePath = filePath
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Calculation')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Omitting CSV file name input
        self.numProcessesInput = QLineEdit(self)
        self.windowInput = QLineEdit(self)
        self.resolutionInput = QLineEdit(self)
        self.outputFileNameInput = QLineEdit(self)
        self.runButton = QPushButton('Run', self)
        self.statusText = QTextEdit(self)
        self.statusText.setReadOnly(True)

        layout.addWidget(QLabel('Number of Processes:'))
        layout.addWidget(self.numProcessesInput)
        layout.addWidget(QLabel('Window:'))
        layout.addWidget(self.windowInput)
        layout.addWidget(QLabel('Resolution:'))
        layout.addWidget(self.resolutionInput)
        layout.addWidget(QLabel('Output File Name:'))
        layout.addWidget(self.outputFileNameInput)
        layout.addWidget(self.runButton)
        layout.addWidget(QLabel('Status:'))
        layout.addWidget(self.statusText)

        self.setLayout(layout)
        self.runButton.clicked.connect(self.runProcessing)

    def runProcessing(self):
        try:
            # Use self.filePath directly
            self.appendStatus(f"Processing file: {self.filePath}")
            self.appendStatus("Starting Processing...")
            # Setup and reading CSV
            XDCRs = read_csv(self.filePath)
            self.appendStatus("CSV file read successfully.")

            # Processing parameters
            num_processes = int(self.numProcessesInput.text())
            window = int(self.windowInput.text())
            resolution = int(self.resolutionInput.text())
            if resolution % num_processes != 0:
                self.appendStatus(f"Resolution must be a multiple of {num_processes}.")
                return

            # Grid generation
            self.appendStatus("Generating Grid...")
            X, Y, Z = generate_grid(window, resolution)

            # 3D Array processing
            self.appendStatus("Processing 3D Array...")
            result = process_3d_array(X, Y, Z, XDCRs, resolution, num_processes)

            # Magnitude and phase calculation
            self.appendStatus("Calculating Magnitude and Phase...")
            result_magnitude, result_phase = calculate_magnitude_phase(result, resolution)

            # Exporting results
            self.appendStatus("Exporting Results...")
            output_csv_filename = self.outputFileNameInput.text()
            output_file_path = os.path.join('OutputFiles', output_csv_filename)
            export_results_to_csv({'X': X, 'Y': Y, 'Z': Z, 'magnitude': result_magnitude, 'phase': result_phase}, output_file_path)

            self.appendStatus("Task Completed Successfully")

        except Exception as e:
            self.appendStatus(f"Error: {str(e)}")

    def appendStatus(self, message):
        self.statusText.append(message)
        QApplication.processEvents()
