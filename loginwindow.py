from PyQt6.QtWidgets import QDialog, QMessageBox, QLineEdit
from PyQt6.QtCore import pyqtSignal, Qt
from ui_loginwindow import Ui_Dialog 

class LoginWindow(QDialog):
    login_successful = pyqtSignal() 

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        self.setWindowTitle("Login to Pet Health Manager")
        self.applyTheme() 
        
        self.ui.login_Btn.clicked.connect(self.check_login)
        self.ui.cancel_Btn.clicked.connect(self.reject) 
        
        self.ui.password_input.setEchoMode(QLineEdit.EchoMode.Password)

    def check_login(self):
        username = self.ui.username_input.text().strip()
        password = self.ui.password_input.text()

        if username == "admin" and password == "admin123": 
            self.login_successful.emit() 
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
            self.ui.password_input.clear() 
            self.ui.username_input.setFocus()

    def applyTheme(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #fdf6f9;
                font-family: 'Segoe UI';
                color: #555555;
            }
            QLabel {
                font-size: 16px;
                font-weight: 700;
                color: #4a2e3a;
                padding-top: 10px;
            }
            QLineEdit {
                background-color: #fff8f9;
                border: 1.5px solid #f4c7d9;
                border-radius: 8px;
                padding: 6px 10px;
            }
            QPushButton {
                background-color: #f9b8c7;
                border: 1.5px solid #f08095;
                border-radius: 10px;
                padding: 8px 16px;
                font-weight: 600;
                color: #4a2e3a;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #f08095;
                color: white;
            }
            QPushButton:pressed {
                background-color: #d56470;
            }
        """)