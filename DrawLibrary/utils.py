import os

class Utils:
    def __init__(self):
        pass

    @staticmethod
    def RemoveFilesInDirectory(directoryPath: str):
        for filename in os.listdir(directoryPath):
            file_path = os.path.join(directoryPath, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)