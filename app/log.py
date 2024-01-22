from PyQt5.QtWidgets import QTextEdit

class ProgressLog(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)

    def print(self, output):
        self.append(f"{output}")