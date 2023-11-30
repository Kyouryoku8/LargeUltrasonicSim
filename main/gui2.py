import sys
import os

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QTabWidget, 
    QFileSystemModel, QTreeView, QWidget, QHBoxLayout, QSplitter,
    QTableWidget, QTableWidgetItem, QLabel, QMenu
)
from PyQt5.QtCore import QDir, Qt, QFileInfo

class MainApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Data Processing GUI')
        self.setGeometry(100, 100, 800, 600)  # Adjust size to match your screenshot
        self.initUI()

    def displaySelectedFile(self, index):
        # Corrected: Use the correct model for each view
        folderModel = self.inputFolderView.model() if self.inputFolderView.hasFocus() else self.outputFolderView.model()
        fileInfo = folderModel.fileInfo(index)
        if fileInfo.isFile() and fileInfo.suffix() == "csv":
            filePath = fileInfo.absoluteFilePath()
            self.loadCsvData(filePath)
            self.fileTitleLabel.setText(fileInfo.fileName())
            self.rightTabWidget.setCurrentWidget(self.dataFileTab)

    def loadCsvData(self, filePath):
        # Load your CSV data into the QTableWidget
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

        # Left splitter for the folder view tabs
        leftTabWidget = QTabWidget()



        # Input Directory Tab
        self.inputFolderView = DataEntryTreeView()  # Create an instance of your custom tree view
        self.inputFolderModel = QFileSystemModel()
        self.inputFolderView.setModel(self.inputFolderModel)
        inputFolderPath = os.path.join(QDir.currentPath(), 'DataFiles')
        self.inputFolderModel.setRootPath(inputFolderPath)
        self.inputFolderView.setRootIndex(self.inputFolderModel.index(inputFolderPath))
        leftTabWidget.addTab(self.inputFolderView, "Input Files")

        # Output Directory Tab
        self.outputFolderView = OutputFilesTreeView()  # Create an instance of your custom tree view
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
        self.rightTabWidget.addTab(QWidget(), "Field Visualization")  # Placeholder for actual content
        # Add more tabs and their content as needed

        # Add rightTabWidget to the main splitter
        mainSplitter.addWidget(self.rightTabWidget)

        # Set the main splitter as the central widget of the window
        self.setCentralWidget(mainSplitter)
        mainSplitter.setSizes([50,600])

        self.inputFolderView.clicked.connect(self.displaySelectedFile)
        self.outputFolderView.clicked.connect(self.displaySelectedFile)

class DataEntryTreeView(QTreeView):
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        viewAction = menu.addAction("View")
        calculateAction = menu.addAction("Calculate")
        deleteAction = menu.addAction("Delete")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        
        # Connect actions to your functions
        if action == viewAction:
            self.viewFile()
        elif action == calculateAction:
            self.calculateFile()
        elif action == deleteAction:
            self.deleteFile()

    def viewFile(self):
        # Implement view functionality
        pass

    def calculateFile(self):
        # Implement calculate functionality
        pass

    def deleteFile(self):
        # Implement delete functionality
        pass

class OutputFilesTreeView(QTreeView):
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        viewAction = menu.addAction("View")
        visualizeAction = menu.addAction("Visualize")
        deleteAction = menu.addAction("Delete")
        action = menu.exec_(self.mapToGlobal(event.pos()))

        # Connect actions to your functions
        if action == viewAction:
            self.viewFile()
        elif action == visualizeAction:
            self.visualizeFile()
        elif action == deleteAction:
            self.deleteFile()

    def viewFile(self):
        # Implement view functionality
        pass

    def visualizeFile(self):
        # Implement visualize functionality
        pass

    def deleteFile(self):
        # Implement delete functionality
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainApplication()
    mainWin.show()
    sys.exit(app.exec_())
