import sys
from PyQt5.QtWidgets import QApplication, QLineEdit, QFormLayout, QWidget, QPushButton

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Azure AI Video Indexer Remux GUI")
        self.resize(500, 150)
        # Create layout
        layout = QFormLayout()
        # Add form components
        api_key = QLineEdit()
        api_key.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow("API Key", api_key)
        layout.addRow("Account ID", QLineEdit())
        layout.addRow("Video URL", QLineEdit())
        layout.addRow(QPushButton("Send to Azure AI Video Indexer"))
        self.setLayout(layout)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
