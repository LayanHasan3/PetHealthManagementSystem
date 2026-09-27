import sys
# --- Database Imports ---
import mysql.connector
from mysql.connector import Error as MySQLError

# --- PyQt6 Imports (Combined) ---
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import (
    QApplication, QDialog, QMainWindow, QWidget, QVBoxLayout, QFormLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QLabel,
    QTabWidget, QDateEdit, QMessageBox, QAbstractItemView, QHeaderView, QTextEdit
)
from PyQt6.QtCore import pyqtSignal, Qt, QDate, QCoreApplication, QMetaObject, QRect, QSize, QTimer

# ====================================================================
# 1. UI_LOGINWINDOW LOGIC (Ui_Dialog)
#    - Renamed to Ui_LoginDialog to avoid confusion.
# ====================================================================
class Ui_LoginDialog(object):
    """Generated UI class for the Login Dialog (from ui_loginwindow.py)"""
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(440, 410)
        self.username_label = QtWidgets.QLabel(parent=Dialog)
        self.username_label.setGeometry(QtCore.QRect(60, 10, 101, 31))
        self.username_label.setObjectName("username_label")
        self.password_label = QtWidgets.QLabel(parent=Dialog)
        self.password_label.setGeometry(QtCore.QRect(60, 86, 91, 31))
        self.password_label.setObjectName("password_label")
        self.username_input = QtWidgets.QLineEdit(parent=Dialog)
        self.username_input.setGeometry(QtCore.QRect(60, 50, 291, 31))
        self.username_input.setObjectName("username_input")
        self.password_input = QtWidgets.QLineEdit(parent=Dialog)
        self.password_input.setGeometry(QtCore.QRect(60, 130, 291, 31))
        self.password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password_input.setObjectName("password_input")
        self.login_Btn = QtWidgets.QPushButton(parent=Dialog)
        self.login_Btn.setGeometry(QtCore.QRect(60, 180, 141, 41))
        self.login_Btn.setObjectName("login_Btn")
        self.cancel_Btn = QtWidgets.QPushButton(parent=Dialog)
        self.cancel_Btn.setGeometry(QtCore.QRect(210, 180, 141, 41))
        self.cancel_Btn.setObjectName("cancel_Btn")
        self.status_label = QtWidgets.QLabel(parent=Dialog)
        self.status_label.setGeometry(QtCore.QRect(60, 230, 291, 41))
        self.status_label.setText("")
        self.status_label.setObjectName("status_label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Login"))
        self.username_label.setText(_translate("Dialog", "Username:"))
        self.password_label.setText(_translate("Dialog", "Password:"))
        self.login_Btn.setText(_translate("Dialog", "Login"))
        self.cancel_Btn.setText(_translate("Dialog", "Cancel"))


# ====================================================================
# 2. LOGINWINDOW CLASS LOGIC (from loginwindow.py)
# ====================================================================
class LoginWindow(QDialog):
    # Signal emitted upon successful login
    login_successful = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Instantiate the UI class (now defined above)
        self.ui = Ui_LoginDialog()
        self.ui.setupUi(self)

        self.setWindowTitle("Login to Pet Health Manager")
        self.applyTheme()

        # --- Connect Signals to Slots ---
        self.ui.login_Btn.clicked.connect(self.check_login)
        self.ui.cancel_Btn.clicked.connect(self.reject) # QDialog built-in reject() closes with Reject status

        # Ensure password field is set to password mode (already done in UI but good practice)
        self.ui.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.ui.username_input.setFocus()

    def check_login(self):
        username = self.ui.username_input.text().strip()
        password = self.ui.password_input.text()

        # --- Hardcoded Authentication Example ---
        if username == "admin" and password == "admin123":
            # DONT call self.accept() here! Just emit the signal.
            self.login_successful.emit()
        elif username == "staff" or password == "staff123":
            self.login_successful.emit()
        else:
            self.ui.status_label.setStyleSheet("color: red; font-weight: bold;")
            self.ui.status_label.setText("Login Failed: Invalid username or password.")
            self.ui.password_input.clear()
            self.ui.username_input.setFocus()


    def applyTheme(self):
        # Reusing the pastel style from your main app for consistency
        self.setStyleSheet("""
            QDialog {
                background-color: #fdf6f9;
                font-family: 'Segoe UI';
                font-size: 14px;
                color: #555555;
            }
            QLabel {
                font-weight: 700;
                color: #4a2e3a;
                padding-top: 10px;
                font-size: 16px;
            }
            QLineEdit {
                background-color: #fff8f9;
                border: 1.5px solid #f4c7d9;
                border-radius: 8px;
                padding: 6px 10px;
                selection-background-color: #f9d5e3;
                color: black;
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
                color: white;
            }
        """)

# ====================================================================
# 3. MAINWINDOW CLASS LOGIC (from mainwindow.py)
# ====================================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.db = None # MySQL Connection Object
        self.cursor = None # MySQL Cursor Object

        if not self.connectDB():
            # If connection fails, the app.py calling logic will stop the app.
            return

        # NOTE: Using the manual setupUI function included below.
        self.setupUI()
        self.setupConnections()
        self.applyPastelTheme()

        # Load initial data from all tables
        self.refreshTable()
        self.refreshMedTable()
        self.refreshVetTable()
        self.refreshVacTable()

    # --- Database Connection ---
    def connectDB(self):
        try:
            self.db = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="pineapple90", # <--- CHANGE THIS TO YOUR ACTUAL PASSWORD!
                database="pethealthdb"
            )
            # Create a cursor for executing queries
            self.cursor = self.db.cursor()
            return True
        except MySQLError as err:
            QMessageBox.critical(
                self, "DB Connection Failed",
                "Could not connect to the MySQL database. "
                "Check credentials, server status, and ensure 'pethealthdb' exists. "
                f"Error: {err}"
            )
            return False

    # --- Manual UI Setup (from mainwindow.py) ---
    def setupUI(self):
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        mainLayout = QVBoxLayout()
        formLayout = QFormLayout()
        buttonLayout = QHBoxLayout()
        searchLayout = QHBoxLayout()

        # Inputs
        self.petID = QLineEdit(); self.petID.setPlaceholderText("Enter Pet ID")
        self.petName = QLineEdit(); self.petName.setPlaceholderText("Enter Name")
        self.petType = QLineEdit(); self.petType.setPlaceholderText("Enter Type")
        self.petBreed = QLineEdit(); self.petBreed.setPlaceholderText("Enter Breed")

        formLayout.addRow("Pet ID:", self.petID)
        formLayout.addRow("Name:", self.petName)
        formLayout.addRow("Type:", self.petType)
        formLayout.addRow("Breed:", self.petBreed)

        # Buttons
        self.addBtn = QPushButton("Add Pet")
        self.updateBtn = QPushButton("Update Pet")
        self.deleteBtn = QPushButton("Delete Pet")
        buttonLayout.addWidget(self.addBtn)
        buttonLayout.addWidget(self.updateBtn)
        buttonLayout.addWidget(self.deleteBtn)

        # Search
        self.searchBox = QLineEdit(); self.searchBox.setPlaceholderText("Search pets...")
        self.searchBtn = QPushButton("Search")
        searchLayout.addWidget(self.searchBox)
        searchLayout.addWidget(self.searchBtn)

        # Pet Table
        self.petTable = QTableWidget(0, 4)
        self.petTable.setHorizontalHeaderLabels(["ID", "Name", "Type", "Breed"])
        self.petTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.petTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.petTable.horizontalHeader().setStretchLastSection(True)

        # Tabs
        self.tabs = QTabWidget()
        self.setupMedTab()
        self.setupVetVisitTab()
        self.setupVaccinationTab()
        self.setupDiagnosisTab()

        # Label
        self.alertLabel = QLabel("Pet Health Management System")
        self.alertLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Assemble
        mainLayout.addLayout(formLayout)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addWidget(self.petTable)
        mainLayout.addLayout(searchLayout)
        mainLayout.addWidget(self.tabs)
        mainLayout.addWidget(self.alertLabel)
        self.centralWidget.setLayout(mainLayout)

        self.setWindowTitle("Pet Medication Tracker")
        self.resize(900, 600)

    def setupMedTab(self):
        self.medTab = QWidget()
        layout = QVBoxLayout()
        inputLayout = QHBoxLayout()

        self.medPetID = QLineEdit(); self.medPetID.setPlaceholderText("Pet ID")
        self.medName = QLineEdit(); self.medName.setPlaceholderText("Medication")
        self.addMedBtn = QPushButton("Add Medication")
        self.removeMedBtn = QPushButton("Remove Medication")

        inputLayout.addWidget(self.medPetID)
        inputLayout.addWidget(self.medName)
        inputLayout.addWidget(self.addMedBtn)
        inputLayout.addWidget(self.removeMedBtn)

        self.medTable = QTableWidget(0, 2)
        self.medTable.setHorizontalHeaderLabels(["Pet ID", "Medication"])
        self.medTable.horizontalHeader().setStretchLastSection(True)

        layout.addLayout(inputLayout)
        layout.addWidget(self.medTable)
        self.medTab.setLayout(layout)
        self.tabs.addTab(self.medTab, "Medications")

    def setupVetVisitTab(self):
        self.vetVisitTab = QWidget()
        layout = QVBoxLayout()
        formLayout = QFormLayout()
        btnLayout = QHBoxLayout()

        self.vetPetID = QLineEdit(); self.vetPetID.setPlaceholderText("Enter Pet ID")
        self.visitDate = QDateEdit(QDate.currentDate())
        self.visitDate.setDisplayFormat("yyyy-MM-dd")
        self.vetNotes = QLineEdit(); self.vetNotes.setPlaceholderText("Reason or notes")

        formLayout.addRow("Pet ID:", self.vetPetID)
        formLayout.addRow("Date:", self.visitDate)
        formLayout.addRow("Notes:", self.vetNotes)

        self.addVetVisitBtn = QPushButton("Add Visit")
        self.removeVetVisitBtn = QPushButton("Remove Visit")
        btnLayout.addWidget(self.addVetVisitBtn)
        btnLayout.addWidget(self.removeVetVisitBtn)

        self.vetTable = QTableWidget(0, 3)
        self.vetTable.setHorizontalHeaderLabels(["Pet ID", "Date", "Notes"])
        self.vetTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout.addLayout(formLayout)
        layout.addLayout(btnLayout)
        layout.addWidget(self.vetTable)
        self.vetVisitTab.setLayout(layout)
        self.tabs.addTab(self.vetVisitTab, "Vet Visits")

    def setupVaccinationTab(self):
        self.vaccinationTab = QWidget()
        layout = QVBoxLayout()
        formLayout = QFormLayout()
        btnLayout = QHBoxLayout()

        self.vacPetID = QLineEdit(); self.vacPetID.setPlaceholderText("Enter Pet ID")
        self.vacName = QLineEdit(); self.vacName.setPlaceholderText("Vaccine Name")
        self.vacDate = QDateEdit(QDate.currentDate())
        self.vacDate.setDisplayFormat("yyyy-MM-dd")

        formLayout.addRow("Pet ID:", self.vacPetID)
        formLayout.addRow("Vaccine:", self.vacName)
        formLayout.addRow("Date Given:", self.vacDate)

        self.addVacBtn = QPushButton("Add Vaccination")
        self.removeVacBtn = QPushButton("Remove Vaccination")
        btnLayout.addWidget(self.addVacBtn)
        btnLayout.addWidget(self.removeVacBtn)

        self.vacTable = QTableWidget(0, 3)
        self.vacTable.setHorizontalHeaderLabels(["Pet ID", "Vaccine", "Date"])
        self.vacTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout.addLayout(formLayout)
        layout.addLayout(btnLayout)
        layout.addWidget(self.vacTable)
        self.vaccinationTab.setLayout(layout)
        self.tabs.addTab(self.vaccinationTab, "Vaccinations")

    def setupDiagnosisTab(self):
        self.diagnosisTab = QWidget()
        layout = QVBoxLayout()
        inputLayout = QHBoxLayout()

        self.diagPetID = QLineEdit()
        self.diagPetID.setPlaceholderText("Enter Pet ID to Generate Report")
        self.generateReportBtn = QPushButton("Generate Health Report")

        inputLayout.addWidget(QLabel("Pet ID:"))
        inputLayout.addWidget(self.diagPetID)
        inputLayout.addWidget(self.generateReportBtn)
        inputLayout.addStretch(1)

        self.reportOutput = QTextEdit()
        self.reportOutput.setReadOnly(True)
        # Initial text with basic styling
        self.reportOutput.setHtml("<p style='font-size: 14px;'>Enter a Pet ID and click 'Generate Health Report' to view a summary of the pet's history.</p>")

        layout.addLayout(inputLayout)
        layout.addWidget(self.reportOutput)
        self.diagnosisTab.setLayout(layout)
        self.tabs.addTab(self.diagnosisTab, "Diagnosis/Report")

    # --- Styling (from mainwindow.py) ---
    def applyPastelTheme(self):
        self.setStyleSheet("""
        QWidget {
            background-color: #fdf6f9;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 14px;
            color: #555555;
        }

        QLineEdit {
            background-color: #fff8f9;
            border: 1.5px solid #f4c7d9;
            border-radius: 8px;
            padding: 6px 10px;
            selection-background-color: #f9d5e3;
        }

        QDateEdit {
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
            min-width: 100px;
        }
        QPushButton:hover {
            background-color: #f08095;
            color: white;
        }
        QPushButton:pressed {
            background-color: #d56470;
            color: white;
        }

        QTableWidget {
            background-color: #fff4f6;
            border: 1px solid #f4c7d9;
            gridline-color: #f9d5e3;
            alternate-background-color: #ffeef2;
            selection-background-color: #f08095;
            selection-color: white;
            border-radius: 10px;
        }
        QHeaderView::section {
            background-color: #f9b8c7;
            color: #4a2e3a;
            padding: 4px;
            border: none;
            font-weight: 700;
        }
        QTabWidget::pane {
            border: 1px solid #f4c7d9;
            border-radius: 12px;
            background: #fff4f6;
        }
        QTabBar::tab {
            background: #f9b8c7;
            color: #4a2e3a;
            padding: 10px 20px;
            border: 1px solid #f4c7d9;
            border-bottom-color: transparent;
            border-top-left-radius: 12px;
            border-top-right-radius: 12px;
            min-width: 120px;
            font-weight: 600;
            margin-right: 2px;
        }
        QTabBar::tab:selected {
            background: #f08095;
            color: white;
            border-color: #d56470;
            border-bottom-color: #fff4f6;
        }
        """)

    # --- Event Connections ---
    def setupConnections(self):
        self.addBtn.clicked.connect(self.addPet)
        self.updateBtn.clicked.connect(self.updatePet)
        self.deleteBtn.clicked.connect(self.deletePet)
        self.searchBtn.clicked.connect(self.searchPet)
        self.addMedBtn.clicked.connect(self.addMedication)
        self.removeMedBtn.clicked.connect(self.removeMedication)
        self.addVetVisitBtn.clicked.connect(self.addVetVisit)
        self.removeVetVisitBtn.clicked.connect(self.removeVetVisit)
        self.addVacBtn.clicked.connect(self.addVaccination)
        self.removeVacBtn.clicked.connect(self.removeVaccination)
        self.petTable.cellClicked.connect(self.onPetSelected)
        self.generateReportBtn.clicked.connect(self.generateReport)

    # --- NEW HELPER FUNCTION ---
    def updateSubTabPetIDs(self, pet_id):
        """Sets the PetID field in all sub-tabs."""
        self.medPetID.setText(pet_id)
        self.vetPetID.setText(pet_id)
        self.vacPetID.setText(pet_id)
        self.diagPetID.setText(pet_id)


    # --- CRUD and Logic Methods (Placeholder for original full logic) ---
    def petExists(self, petId):
        try:
            self.cursor.execute("SELECT PetID FROM Pets WHERE PetID = %s", (petId,))
            return self.cursor.fetchone() is not None
        except MySQLError as err:
            QMessageBox.critical(self, "DB Error", f"Pet existence check failed: {err}")
            return False

    def addPet(self):
        # Full logic for adding a pet goes here
        pet_id = self.petID.text()
        pet_name = self.petName.text()
        pet_type = self.petType.text()
        pet_breed = self.petBreed.text()
        if not pet_id or not pet_name:
            self.alertLabel.setText("Error: Pet ID and Name are required.")
            return

        query = "INSERT INTO Pets (PetID, Name, Type, Breed) VALUES (%s, %s, %s, %s)"
        try:
            self.cursor.execute(query, (pet_id, pet_name, pet_type, pet_breed))
            self.db.commit()
            self.alertLabel.setText(f"Pet '{pet_name}' added successfully.")
            self.refreshTable()
        except MySQLError as err:
            self.alertLabel.setText(f"Error adding pet: {err}")

    def updatePet(self):
        # Full logic for updating a pet goes here
        pet_id = self.petID.text()
        pet_name = self.petName.text()
        pet_type = self.petType.text()
        pet_breed = self.petBreed.text()
        if not pet_id:
            self.alertLabel.setText("Error: Pet ID is required for update.")
            return

        query = "UPDATE Pets SET Name = %s, Type = %s, Breed = %s WHERE PetID = %s"
        try:
            self.cursor.execute(query, (pet_name, pet_type, pet_breed, pet_id))
            self.db.commit()
            if self.cursor.rowcount > 0:
                self.alertLabel.setText(f"Pet ID {pet_id} updated successfully.")
                self.refreshTable()
            else:
                self.alertLabel.setText(f"Pet ID {pet_id} not found.")
        except MySQLError as err:
            self.alertLabel.setText(f"Error updating pet: {err}")

    def deletePet(self):
        # Full logic for deleting a pet goes here
        pet_id = self.petID.text()
        if not pet_id:
            self.alertLabel.setText("Error: Pet ID is required for deletion.")
            return

        confirm = QMessageBox.question(self, 'Confirm Deletion',
                                       f"Are you sure you want to delete Pet with {pet_id} and ALL related records?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                # Deleting from all related tables (Medication, VetVisits, Vaccinations) should be handled via foreign keys ON DELETE CASCADE in the DB schema, but for safety, we include explicit deletes if not
                self.cursor.execute("DELETE FROM Medications WHERE PetID = %s", (pet_id,))
                self.cursor.execute("DELETE FROM VetVisits WHERE PetID = %s", (pet_id,))
                self.cursor.execute("DELETE FROM Vaccinations WHERE PetID = %s", (pet_id,))
                self.cursor.execute("DELETE FROM Pets WHERE PetID = %s", (pet_id,))
                self.db.commit()
                if self.cursor.rowcount > 0:
                    self.alertLabel.setText(f"Pet ID {pet_id} and all related records deleted.")
                    self.refreshTable()
                    self.petID.clear(); self.petName.clear(); self.petType.clear(); self.petBreed.clear()
                else:
                    self.alertLabel.setText(f"Pet ID {pet_id} not found.")
            except MySQLError as err:
                self.alertLabel.setText(f"Error deleting pet: {err}")

    def searchPet(self):
        # Full logic for searching pets goes here
        search_text = self.searchBox.text().strip()
        if not self.db or not self.cursor:
            self.alertLabel.setText("Error: Database connection failed.")
            return

        search_pattern = f"%{search_text}%"
        query = """
              SELECT PetID, Name, Type, Breed
              FROM Pets
              WHERE PetID LIKE %s OR Name LIKE %s OR Type LIKE %s OR Breed LIKE %s
              ORDER BY PetID
        """
        values = (search_pattern, search_pattern, search_pattern, search_pattern)

        try:
            self.cursor.execute(query, values)
            data = self.cursor.fetchall()

            self.petTable.setRowCount(0)
            for row, row_data in enumerate(data):
                self.petTable.insertRow(row)
                for col, value in enumerate(row_data):
                    self.petTable.setItem(row, col, QTableWidgetItem(str(value)))

            self.alertLabel.setText(f"{len(data)} pets found matching '{search_text}'.")
        except MySQLError as err:
            QMessageBox.critical(self, "DB Error", f"Search failed: {err}")

    def onPetSelected(self, row, _):
        # Existing logic to populate main inputs and sub-tab inputs upon selection
        pet_id = self.petTable.item(row, 0).text()
        self.petID.setText(pet_id)
        self.petName.setText(self.petTable.item(row, 1).text())
        self.petType.setText(self.petTable.item(row, 2).text())
        self.petBreed.setText(self.petTable.item(row, 3).text())

        # Update sub-tab inputs
        self.updateSubTabPetIDs(pet_id)

        # Refresh sub-tables for the selected pet
        self.refreshMedTable(pet_id)
        self.refreshVetTable(pet_id)
        self.refreshVacTable(pet_id)
        # Clear report output on new selection
        self.reportOutput.clear()


    # --- Refresh/Load Data Methods ---

    def refreshTable(self):
        """Refreshes the main Pets table."""
        if not self.db or not self.cursor: return

        try:
            self.cursor.execute("SELECT PetID, Name, Type, Breed FROM Pets ORDER BY PetID")
            data = self.cursor.fetchall()

            self.petTable.setRowCount(0)
            for row, row_data in enumerate(data):
                self.petTable.insertRow(row)
                for col, value in enumerate(row_data):
                    self.petTable.setItem(row, col, QTableWidgetItem(str(value)))
        except MySQLError as err:
            QMessageBox.critical(self, "DB Error", f"Failed to load pets: {err}")

    def refreshMedTable(self, pet_id=None):
        """Refreshes the Medications table, optionally filtering by pet_id."""
        if not self.db or not self.cursor: return
        query = "SELECT PetID, MedicationName FROM Medications"
        if pet_id:
            query += " WHERE PetID = %s"
            values = (pet_id,)
        else:
            values = None

        try:
            self.cursor.execute(query, values)
            data = self.cursor.fetchall()

            self.medTable.setRowCount(0)
            for row, row_data in enumerate(data):
                self.medTable.insertRow(row)
                for col, value in enumerate(row_data):
                    self.medTable.setItem(row, col, QTableWidgetItem(str(value)))
        except MySQLError as err:
            QMessageBox.critical(self, "DB Error", f"Failed to load Medications: {err}")

    def refreshVetTable(self, pet_id=None):
        """Refreshes the Vet Visits table, optionally filtering by pet_id."""
        if not self.db or not self.cursor: return
        query = "SELECT PetID, VisitDate, Notes FROM VetVisits"
        if pet_id:
            query += " WHERE PetID = %s"
            values = (pet_id,)
        else:
            values = None

        try:
            self.cursor.execute(query, values)
            data = self.cursor.fetchall()

            self.vetTable.setRowCount(0)
            for row, row_data in enumerate(data):
                self.vetTable.insertRow(row)
                for col, value in enumerate(row_data):
                    self.vetTable.setItem(row, col, QTableWidgetItem(str(value)))
        except MySQLError as err:
            QMessageBox.critical(self, "DB Error", f"Failed to load vet visits: {err}")

    def refreshVacTable(self, pet_id=None):
        """Refreshes the Vaccinations table, optionally filtering by pet_id."""
        if not self.db or not self.cursor: return
        query = "SELECT PetID, VaccineName, DateGiven FROM Vaccinations"
        if pet_id:
            query += " WHERE PetID = %s"
            values = (pet_id,)
        else:
            values = None

        try:
            self.cursor.execute(query, values)
            data = self.cursor.fetchall()

            self.vacTable.setRowCount(0)
            for row, row_data in enumerate(data):
                self.vacTable.insertRow(row)
                for col, value in enumerate(row_data):
                    self.vacTable.setItem(row, col, QTableWidgetItem(str(value)))
        except MySQLError as err:
            QMessageBox.critical(self, "DB Error", f"Failed to load vaccinations: {err}")


    # --- Sub-Tab CRUD Methods ---
    def addMedication(self):
        pet_id = self.medPetID.text().strip()
        med_name = self.medName.text().strip()
        if not pet_id or not med_name:
            QMessageBox.warning(self, "Input Error", "Both Pet ID and Medication Name are required.")
            return

        if not self.petExists(pet_id):
            QMessageBox.warning(self, "Validation Error", f"Pet ID {pet_id} does not exist.")
            return

        try:
            query = "INSERT INTO Medications (PetID, MedicationName) VALUES (%s, %s)"
            self.cursor.execute(query, (pet_id, med_name))
            self.db.commit()
            self.alertLabel.setText(f"Medications '{med_name}' added for Pet ID {pet_id}.")
            self.refreshMedTable(pet_id)
            self.medName.clear()
        except MySQLError as err:
            QMessageBox.critical(self, "DB Error", f"Error adding medications: {err}")

    def removeMedication(self):
        selected_rows = self.medTable.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Selection Error", "Please select a medication to remove.")
            return

        # Assumes only one row is selected
        row = selected_rows[0].row()
        pet_id = self.medTable.item(row, 0).text()
        med_name = self.medTable.item(row, 1).text()

        confirm = QMessageBox.question(self, 'Confirm Deletion',
                                       f"Are you sure you want to remove '{med_name}' for Pet ID {pet_id}?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                # Assuming (PetID, MedicationName) is unique or we delete the first match
                query = "DELETE FROM Medications WHERE PetID = %s AND MedicationName = %s LIMIT 1"
                self.cursor.execute(query, (pet_id, med_name))
                self.db.commit()
                self.alertLabel.setText(f"Medications '{med_name}' removed for Pet ID {pet_id}.")
                self.refreshMedTable(pet_id)
            except MySQLError as err:
                QMessageBox.critical(self, "DB Error", f"Error removing medications: {err}")

    def addVetVisit(self):
        pet_id = self.vetPetID.text().strip()
        visit_date = self.visitDate.date().toString("yyyy-MM-dd")
        notes = self.vetNotes.text().strip()
        if not pet_id or not notes:
            QMessageBox.warning(self, "Input Error", "Pet ID, Date, and Notes are required.")
            return

        if not self.petExists(pet_id):
            QMessageBox.warning(self, "Validation Error", f"Pet ID {pet_id} does not exist.")
            return

        try:
            query = "INSERT INTO VetVisits (PetID, VisitDate, Notes) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (pet_id, visit_date, notes))
            self.db.commit()
            self.alertLabel.setText(f"Visit added for Pet ID {pet_id} on {visit_date}.")
            self.refreshVetTable(pet_id)
            self.vetNotes.clear()
        except MySQLError as err:
            QMessageBox.critical(self, "DB Error", f"Error adding vet visit: {err}")

    def removeVetVisit(self):
        selected_rows = self.vetTable.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Selection Error", "Please select a visit to remove.")
            return

        row = selected_rows[0].row()
        pet_id = self.vetTable.item(row, 0).text()
        visit_date = self.vetTable.item(row, 1).text()
        notes = self.vetTable.item(row, 2).text() # Use notes as an extra identifier for the unique row

        confirm = QMessageBox.question(self, 'Confirm Deletion',
                                       f"Are you sure you want to remove the visit on {visit_date} for Pet ID {pet_id}?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                # Deleting by the unique combination of PetID, Date, and Notes
                query = "DELETE FROM VetVisits WHERE PetID = %s AND VisitDate = %s AND Notes = %s LIMIT 1"
                self.cursor.execute(query, (pet_id, visit_date, notes))
                self.db.commit()
                self.alertLabel.setText(f"Vet visit removed for Pet ID {pet_id} on {visit_date}.")
                self.refreshVetTable(pet_id)
            except MySQLError as err:
                QMessageBox.critical(self, "DB Error", f"Error removing vet visit: {err}")

    def addVaccination(self):
        pet_id = self.vacPetID.text().strip()
        vac_name = self.vacName.text().strip()
        vac_date = self.vacDate.date().toString("yyyy-MM-dd")
        if not pet_id or not vac_name:
            QMessageBox.warning(self, "Input Error", "Pet ID and Vaccine Name are required.")
            return

        if not self.petExists(pet_id):
            QMessageBox.warning(self, "Validation Error", f"Pet ID {pet_id} does not exist.")
            return

        try:
            query = "INSERT INTO Vaccinations (PetID, VaccineName, DateGiven) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (pet_id, vac_name, vac_date))
            self.db.commit()
            self.alertLabel.setText(f"Vaccination '{vac_name}' added for Pet ID {pet_id} on {vac_date}.")
            self.refreshVacTable(pet_id)
            self.vacName.clear()
        except MySQLError as err:
            QMessageBox.critical(self, "DB Error", f"Error adding vaccination: {err}")

    def removeVaccination(self):
        selected_rows = self.vacTable.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Selection Error", "Please select a vaccination to remove.")
            return

        row = selected_rows[0].row()
        pet_id = self.vacTable.item(row, 0).text()
        vac_name = self.vacTable.item(row, 1).text()
        vac_date = self.vacTable.item(row, 2).text()

        confirm = QMessageBox.question(self, 'Confirm Deletion',
                                       f"Are you sure you want to remove '{vac_name}' on {vac_date} for Pet ID {pet_id}?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                # Deleting by the unique combination of PetID, VaccineName, and Date
                query = "DELETE FROM Vaccinations WHERE PetID = %s AND VaccineName = %s AND DateGiven = %s LIMIT 1"
                self.cursor.execute(query, (pet_id, vac_name, vac_date))
                self.db.commit()
                self.alertLabel.setText(f"Vaccination '{vac_name}' removed for Pet ID {pet_id}.")
                self.refreshVacTable(pet_id)
            except MySQLError as err:
                QMessageBox.critical(self, "DB Error", f"Error removing vaccination: {err}")

    def generateReport(self):
        pet_id = self.diagPetID.text().strip()
        self.reportOutput.clear()

        if not pet_id:
            self.reportOutput.setHtml("<p style='color: red;'>Please enter a Pet ID.</p>")
            return

        # 1. Get Pet Information
        try:
            self.cursor.execute("SELECT Name, Type, Breed FROM Pets WHERE PetID = %s", (pet_id,))
            pet_info = self.cursor.fetchone()
        except MySQLError as err:
            self.reportOutput.setHtml(f"<p style='color: red;'>DB Error: {err}</p>")
            return

        if not pet_info:
            self.reportOutput.setHtml(f"<p style='color: red;'>Pet ID {pet_id} not found.</p>")
            return

        name, pet_type, breed = pet_info

        report_html = f"""
            <h2 style='color: #4a2e3a;'>Health Report for {name} (ID: {pet_id})</h2>
            <p style='font-weight: 600;'>Type: {pet_type}, Breed: {breed}</p>
            <hr>
        """

        # 2. Get Medications
        try:
            self.cursor.execute("SELECT MedicationName FROM Medication WHERE PetID = %s", (pet_id,))
            meds = [row[0] for row in self.cursor.fetchall()]
            report_html += "<h3 style='color: #f08095;'>Current Medications</h3>"
            if meds:
                report_html += "<ul>" + "".join([f"<li>{m}</li>" for m in meds]) + "</ul>"
            else:
                report_html += "<p>No medications recorded.</p>"
        except MySQLError: pass

        # 3. Get Vet Visits
        try:
            self.cursor.execute("SELECT VisitDate, Notes FROM VetVisits WHERE PetID = %s ORDER BY VisitDate DESC", (pet_id,))
            visits = self.cursor.fetchall()
            report_html += "<h3 style='color: #f08095;'>Vet Visit History</h3>"
            if visits:
                report_html += "<ul>"
                for date, notes in visits:
                    report_html += f"<li><strong>{date.strftime('%Y-%m-%d')}:</strong> {notes}</li>"
                report_html += "</ul>"
            else:
                report_html += "<p>No vet visits recorded.</p>"
        except MySQLError: pass

        # 4. Get Vaccinations
        try:
            self.cursor.execute("SELECT VaccineName, DateGiven FROM Vaccinations WHERE PetID = %s ORDER BY DateGiven DESC", (pet_id,))
            vaccines = self.cursor.fetchall()
            report_html += "<h3 style='color: #f08095;'>Vaccination Record</h3>"
            if vaccines:
                report_html += "<ul>"
                for name, date in vaccines:
                    report_html += f"<li><strong>{name}:</strong> {date.strftime('%Y-%m-%d')}</li>"
                report_html += "</ul>"
            else:
                report_html += "<p>No vaccinations recorded.</p>"
        except MySQLError: pass

        self.reportOutput.setHtml(report_html)

# ====================================================================
# 4. APPLICATION ENTRY POINT (from app.py)
# ====================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 1. Start with the Login Window
    login_win = LoginWindow()

    # --- Setup the successful login action ---
    # When the custom signal is emitted, we close the dialog successfully (QDialog.Accepted).
    login_win.login_successful.connect(login_win.accept)

    # Execute the login dialog. This call BLOCKS until accept() or reject() is called.
    login_result = login_win.exec()

    # Check the result of the login dialog
    if login_result == QDialog.DialogCode.Accepted:
        # 2. Login was successful, now launch the main application window

        main_win = MainWindow()

        # Crucial check to ensure DB connection passed before showing the main window
        if main_win.db is not None:
            # Show the window and enter the main application event loop
            main_win.show()
            sys.exit(app.exec())
        else:
            # DB connection failed within MainWindow.__init__
            QMessageBox.critical(
                None, "Fatal Error",
                "Database connection failed. Application terminating."
            )
            sys.exit(1)

    else:
        # 3. Login was cancelled or rejected
        sys.exit(0)