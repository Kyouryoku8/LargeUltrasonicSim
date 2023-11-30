import sys
import os
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from PyQt5.QtWidgets import QApplication, QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox, QSizePolicy, QMainWindow, QVBoxLayout, QTabWidget, QFileSystemModel, QWidget, QHBoxLayout, QSplitter, QTableWidget, QTableWidgetItem, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import QDir, Qt
from data_entry_tree_view import DataEntryTreeView
from output_files_tree_view import OutputFilesTreeView
from data_processing import DataProcessor


class MainApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Data Processing GUI')
        self.setGeometry(100, 100, 800, 600)  
        self.initUI()

    def displaySelectedFile(self, index):
        folderModel = self.inputFolderView.model() if self.inputFolderView.hasFocus() else self.outputFolderView.model()
        fileInfo = folderModel.fileInfo(index)
        if fileInfo.isFile() and fileInfo.suffix() == "csv":
            filePath = fileInfo.absoluteFilePath()
            self.loadCsvData(filePath)
            self.fileTitleLabel.setText(fileInfo.fileName())
            self.rightTabWidget.setCurrentWidget(self.dataFileTab)

    def loadCsvData(self, filePath):
        # Load CSV data into the QTableWidget
        with open(filePath, 'r', encoding='utf-8-sig') as file:
            content = file.readlines()

        # Clear the table first
        self.dataFileTable.clear()
        self.dataFileTable.setRowCount(0)

        # Assume first line is header
        header = content[0].strip().split(',')
        self.dataFileTable.setColumnCount(len(header))
        self.dataFileTable.setHorizontalHeaderLabels(header)

        # Set the rest of the data
        for row_index, row_data in enumerate(content[1:]):
            row_data = row_data.strip().split(',')
            self.dataFileTable.insertRow(row_index)
            for column_index, data in enumerate(row_data):
                self.dataFileTable.setItem(row_index, column_index, QTableWidgetItem(data))

    def initUI(self):
        self.setWindowTitle('Data Processing GUI')
        self.setGeometry(100, 100, 1280, 720)

        # Main splitter
        mainSplitter = QSplitter(Qt.Horizontal)

        menuBar = self.menuBar()
        optionsMenu = menuBar.addMenu('Options')
        helpMenu = menuBar.addMenu('Help')
        mainSplitter = QSplitter(Qt.Horizontal)

        aboutAction = helpMenu.addAction('About')
        aboutAction.triggered.connect(self.showHelpPopup)

        # Left splitter for the folder view tabs
        leftTabWidget = QTabWidget()

        # Input Directory Tab
        self.inputFolderView = DataEntryTreeView()  # Create an instance of custom tree view
        self.inputFolderModel = QFileSystemModel()
        self.inputFolderView.setModel(self.inputFolderModel)
        inputFolderPath = os.path.join(QDir.currentPath(), 'DataFiles')
        self.inputFolderModel.setRootPath(inputFolderPath)
        self.inputFolderView.setRootIndex(self.inputFolderModel.index(inputFolderPath))
        leftTabWidget.addTab(self.inputFolderView, "Input Files")

        # Output Directory Tab
        self.outputFolderView = OutputFilesTreeView()  # Create an instance of custom tree view
        self.outputFolderModel = QFileSystemModel()
        self.outputFolderView.setModel(self.outputFolderModel)
        outputFolderPath = os.path.join(QDir.currentPath(), 'OutputFiles')
        self.outputFolderModel.setRootPath(outputFolderPath)
        self.outputFolderView.setRootIndex(self.outputFolderModel.index(outputFolderPath))
        leftTabWidget.addTab(self.outputFolderView, "Output Files")


        # Add leftTabWidget to the main splitter
        mainSplitter.addWidget(leftTabWidget)
        

        # Right tab widget for additional information or controls
        self.rightTabWidget = QTabWidget()
        self.dataFileTab = QWidget()
        self.dataFileLayout = QVBoxLayout()
        self.fileTitleLabel = QLabel("Select a file to view its contents")
        self.dataFileTable = QTableWidget()
        self.dataFileLayout.addWidget(self.fileTitleLabel)
        self.dataFileLayout.addWidget(self.dataFileTable)
        self.dataFileTab.setLayout(self.dataFileLayout)
        self.rightTabWidget.addTab(self.dataFileTab, "Data File")
        self.rightTabWidget.addTab(QWidget(), "Field Visualization") 
        # Add more tabs and content as needed

        # Add rightTabWidget to the main splitter
        mainSplitter.addWidget(self.rightTabWidget)

        # Set the main splitter as the central widget of the window
        self.setCentralWidget(mainSplitter)
        mainSplitter.setSizes([50,600])

        self.inputFolderView.clicked.connect(self.displaySelectedFile)
        self.outputFolderView.clicked.connect(self.displaySelectedFile)

        settingsAction = optionsMenu.addAction('Settings')
        settingsAction.triggered.connect(self.showSettingsDialog)        

    def showSettingsDialog(self):
        dialog = SettingsDialog(self)
        if dialog.exec_():
            width, height = dialog.getSettings()
            self.resize(width, height)

    def showHelpPopup(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("About")
        msgBox.setText("Welcome to LargeUltrasonicSIM\n\n"
                       "You can view the .csv in table format by selecting view when right clicking an input file\n\n"
                       "You can run a simulation based on user defined parameters by selecting calculate when right clicking an input file\n\n"
                       "You can visualize the output by right-clicking your output file and selecting visualize"
                       )
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()

    def visualizeData(self, filePath, target_z = 200):
        filtered_data = DataProcessor.filter_data_by_z(filePath, target_z)
        X, Y, Z = DataProcessor.get_xyz_from_data(filtered_data)

        x_min, x_max = X.min(), X.max()
        y_min, y_max = Y.min(), Y.max()
        z_min, z_max = Z.min(), Z.max()        

        x_margin = (x_max - x_min) * 0.1
        y_margin = (y_max - y_min) * 0.1
        z_margin = (z_max - z_min) * 0.1

        # Create a matplotlib canvas
        canvas = FigureCanvas(Figure(figsize=(5, 3)))
        ax = canvas.figure.add_subplot(111, projection='3d')
        ax.plot_trisurf(X, Y, Z, linewidth=0, edgecolor='none')

        # Set axis limits
        ax.set_xlim([x_min - x_margin, x_max + x_margin])
        ax.set_ylim([y_min - y_margin, y_max + y_margin])
        ax.set_zlim([z_min - z_margin, z_max + z_margin])

        ax.set_title("XDCR Amplitude")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Amplitude")

        # Clear the previous plot and set the new one
        vizTab = self.rightTabWidget.widget(1) 

        # Clear the existing layout
        self.clearLayout(vizTab.layout())

        # Set the new layout with the matplotlib canvas
        newLayout = QVBoxLayout()
        newLayout.addWidget(canvas)
        vizTab.setLayout(newLayout)

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            QWidget().setLayout(layout)

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.setWindowTitle('Settings')

        # Create form layout
        layout = QFormLayout(self)

        # Add window width setting
        self.widthInput = QLineEdit(self)
        self.widthInput.setPlaceholderText("Enter window width")
        layout.addRow("Width:", self.widthInput)

        # Add window height setting
        self.heightInput = QLineEdit(self)
        self.heightInput.setPlaceholderText("Enter window height")
        layout.addRow("Height:", self.heightInput)

        # Add buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def getSettings(self):
        return int(self.widthInput.text()), int(self.heightInput.text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainApplication()
    mainWin.show()
    sys.exit(app.exec_())
