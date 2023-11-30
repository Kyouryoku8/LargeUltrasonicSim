import sys
import os
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from PyQt5.QtWidgets import QApplication, QSizePolicy, QMainWindow, QVBoxLayout, QTabWidget, QFileSystemModel, QWidget, QHBoxLayout, QSplitter, QTableWidget, QTableWidgetItem, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import QDir, Qt
from data_entry_tree_view import DataEntryTreeView
from output_files_tree_view import OutputFilesTreeView

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

    def visualizeData(self, filePath, target_z = 200):
        # Read the data
        data = pd.read_csv(filePath)
        filtered_data = data[data['Z'] == target_z]
        X = np.array(filtered_data['X'].tolist())
        Y = np.array(filtered_data['Y'].tolist())
        Z = np.array(filtered_data['Magnitude'].tolist())

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainApplication()
    mainWin.show()
    sys.exit(app.exec_())