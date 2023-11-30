from PyQt5.QtWidgets import QTreeView, QMenu
from calculation_dialog import CalculationDialog
from file_utils import FileUtils

class DataEntryTreeView(QTreeView):
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        viewAction = menu.addAction("View")
        calculateAction = menu.addAction("Calculate")
        deleteAction = menu.addAction("Delete")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        
        # Connect actions tofunctions
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
        index = self.currentIndex()
        if index.isValid():
            model = self.model()
            fileInfo = model.fileInfo(index)
            if fileInfo.isFile() and fileInfo.suffix() == "csv":
                filePath = fileInfo.absoluteFilePath()
                dialog = CalculationDialog(filePath, self)
                dialog.exec_()

    def deleteFile(self):
        index = self.currentIndex()
        if index.isValid():
            model = self.model()
            fileInfo = model.fileInfo(index)
            if fileInfo.isFile():
                filePath = fileInfo.absoluteFilePath()
                success, message = FileUtils.deleteFile(filePath)
                # Handle the response, e.g., show a message box or update status
