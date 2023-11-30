import os

class FileUtils:
    @staticmethod
    def deleteFile(filePath):
        try:
            os.remove(filePath)
            return True, "File deleted successfully."
        except FileNotFoundError:
            return False, "File not found."
        except PermissionError:
            return False, "Permission denied."
        except Exception as e:
            return False, str(e)
