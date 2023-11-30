# output_files_tree_view.py

from PyQt5.QtWidgets import QTreeView, QMenu
from file_utils import FileUtils

class OutputFilesTreeView(QTreeView):
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        viewAction = menu.addAction("View")
        visualizeAction = menu.addAction("Visualize")
        deleteAction = menu.addAction("Delete")
        action = menu.exec_(self.mapToGlobal(event.pos()))

        # Connect actions to functions
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
        index = self.currentIndex()
        if index.isValid():
            model = self.model()
            fileInfo = model.fileInfo(index)
            if fileInfo.isFile():
                filePath = fileInfo.absoluteFilePath()
                success, message = FileUtils.deleteFile(filePath)
                # Handle the response, e.g., show a message box or update status
