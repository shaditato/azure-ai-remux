from .log import ProgressLog
import sys
from PyQt5.QtWidgets import QApplication, QDialogButtonBox, QFormLayout, QLineEdit, QStyle, QTextEdit, QWidget

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Configure window
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
        # Add output box
        log_edit = ProgressLog()
        log_edit.print("<Progress updates will go here>")
        layout.addRow(log_edit)
        # Add submit/cancel buttons
        button_box = QDialogButtonBox()
        accept_btn = button_box.addButton("Send to Azure AI Video Indexer", QDialogButtonBox.ButtonRole.AcceptRole)
        accept_icon = self.style().standardIcon(QStyle.SP_DialogApplyButton)
        accept_btn.setIcon(accept_icon)
        button_box.addButton(QDialogButtonBox.StandardButton.Cancel)
        button_box.clicked.connect(lambda btn: self.handleButtonClick(btn, button_box))
        layout.addRow(button_box)
        # Set layout
        self.setLayout(layout)
    
    def handleButtonClick(self, button, button_box):
        role = button_box.buttonRole(button)
        if role == QDialogButtonBox.ButtonRole.AcceptRole:
            print("applied")
            # link Azure functions
        elif role == QDialogButtonBox.ButtonRole.RejectRole:
            self.close()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
