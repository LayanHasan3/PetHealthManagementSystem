import sys
import mysql.connector
from mysql.connector import Error as MySQLError
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QLabel,
    QTabWidget, QDateEdit, QMessageBox, QAbstractItemView, QHeaderView, QTextEdit
)
from PyQt6.QtCore import QDate, Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = None
        self.cursor = None

        if not self.connectDB():
            return 

        self.setupUI() 
        self.setupConnections()
        self.applyPastelTheme()

        self.refreshTable()
        self.refreshMedTable()
        self.refreshVetTable()
        self.refreshVacTable()

    def connectDB(self):
        try:
            self.db = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="pineapple90",
                database="pethealthdb" 
            )
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

    def setupUI(self):
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        mainLayout = QVBoxLayout()
        formLayout = QFormLayout()
        buttonLayout = QHBoxLayout()
        searchLayout = QHBoxLayout()

        self.petID = QLineEdit(); self.petID.setPlaceholderText("Enter Pet ID")
        self.petName = QLineEdit(); self.petName.setPlaceholderText("Enter Name")
        self.petType = QLineEdit(); self.petType.setPlaceholderText("Enter Type")
        self.petBreed = QLineEdit(); self.petBreed.setPlaceholderText("Enter Breed")

        formLayout.addRow("Pet ID:", self.petID)
        formLayout.addRow("Name:", self.petName)
        formLayout.addRow("Type:", self.petType)
        formLayout.addRow("Breed:", self.petBreed)

        self.addBtn = QPushButton("Add Pet")
        self.updateBtn = QPushButton("Update Pet")
        self.deleteBtn = QPushButton("Delete Pet")
        buttonLayout.addWidget(self.addBtn)
        buttonLayout.addWidget(self.updateBtn)
        buttonLayout.addWidget(self.deleteBtn)

        self.searchBox = QLineEdit(); self.searchBox.setPlaceholderText("Search pets...")
        self.searchBtn = QPushButton("Search")
        searchLayout.addWidget(self.searchBox)
        searchLayout.addWidget(self.searchBtn)

        self.petTable = QTableWidget(0, 4)
        self.petTable.setHorizontalHeaderLabels(["ID", "Name", "Type", "Breed"])
        self.petTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.petTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.petTable.horizontalHeader().setStretchLastSection(True)

        self.tabs = QTabWidget()
        self.setupMedTab()
        self.setupVetVisitTab()
        self.setupVaccinationTab()
        self.setupDiagnosisTab()

        self.alertLabel = QLabel("Pet Health Management System")
        self.alertLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

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
        self.reportOutput.setHtml("<p style='font-size: 14px;'>Enter a Pet ID and click 'Generate Health Report' to view a summary of the pet's history.</p>")

        layout.addLayout(inputLayout)
        layout.addWidget(self.reportOutput)
        self.diagnosisTab.setLayout(layout)
        self.tabs.addTab(self.diagnosisTab, "Diagnosis/Report")

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

    def updateSubTabPetIDs(self, pet_id):
        self.medPetID.setText(pet_id)
        self.vetPetID.setText(pet_id)
        self.vacPetID.setText(pet_id)
        self.diagPetID.setText(pet_id)
    

    def petExists(self, petId):
        try:
            self.cursor.execute("SELECT PetID FROM Pets WHERE PetID = %s", (petId,))
            return self.cursor.fetchone() is not None
        except MySQLError as err:
            QMessageBox.critical(self, "DB Error", f"Pet existence check failed: {err}")
            return False

    def addPet(self):
        id_ = self.petID.text().strip()
        name = self.petName.text().strip()
        type_ = self.petType.text().strip()
        breed = self.petBreed.text().strip()
        
        if not id_ or not name:
            QMessageBox.warning(self, "Input Error", "Pet ID and Name required!")
            return
        
        query = "INSERT INTO Pets (PetID, Name, Type, Breed) VALUES (%s, %s, %s, %s)"
        values = (id_, name, type_, breed)
        
        try:
            self.cursor.execute(query, values)
            self.db.commit()
            self.alertLabel.setText(f"Pet {name} added successfully!")
            self.refreshTable()
            
            self.updateSubTabPetIDs(id_)
            
        except MySQLError as err:
            QMessageBox.critical(self, "DB Error", f"Failed to add pet: {err}")

    def updatePet(self):
        id_ = self.petID.text().strip()
        name = self.petName.text().strip()
        type_ = self.petType.text().strip()
        breed = self.petBreed.text().strip()

        if not self.petTable.selectedItems():
            QMessageBox.warning(self, "Selection Error", "Please select a pet to update.")
            return

        query = "UPDATE Pets SET Name = %s, Type = %s, Breed = %s WHERE PetID = %s"
        values = (name, type_, breed, id_)

        try:
            self.cursor.execute(query, values)
            self.db.commit()
            if self.cursor.rowcount > 0:
                self.alertLabel.setText(f"Pet {name} updated successfully!")
                self.refreshTable()
            else:
                 QMessageBox.warning(self, "Update Failed", "Pet ID not found or no changes made.")
        except MySQLError as err:
            QMessageBox.critical(self, "DB Error", f"Failed to update pet: {err}")
            
    def deletePet(self):
        if not self.petTable.selectedItems():
            QMessageBox.warning(self, "Selection Error", "Please select a pet to delete.")
            return
        
        id_ = self.petID.text().strip()
        name = self.petName.text().strip()

        reply = QMessageBox.question(self, 'Confirm Delete',
            f"Are you sure you want to delete Pet ID: {id_} ({name})? This will also delete ALL associated medication, vet_visit_history, and vaccinations.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            query = "DELETE FROM Pets WHERE PetID = %s"
            try:
                self.cursor.execute(query, (id_,))
                self.db.commit()
                self.alertLabel.setText(f"Pet {name} and all related records deleted.")
                self.refreshTable()
                self.refreshMedTable()
                self.refreshVetTable()
                self.refreshVacTable()

                self.updateSubTabPetIDs("") 

            except MySQLError as err:
                QMessageBox.critical(self, "DB Error", f"Failed to delete pet: {err}")

    def refreshTable(self):
        query = "SELECT PetID, Name, Type, Breed FROM Pets ORDER BY PetID"
        try:
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            
            self.petTable.setRowCount(0)
            for row, row_data in enumerate(data):
                self.petTable.insertRow(row)
                for col, value in enumerate(row_data):
                    self.petTable.setItem(row, col, QTableWidgetItem(str(value)))
        except MySQLError as err:
            QMessageBox.critical(self, "DB Error", f"Failed to refresh Pets table: {err}")

    def addMedication(self):
        pet_id = self.medPetID.text().strip()
        med_name = self.medName.text().strip()

        if not pet_id or not med_name:
            QMessageBox.warning(self, "Input Error", "Pet ID and Medication Name required.")
            return
        if not self.petExists(pet_id):
            QMessageBox.critical(self, "Input Error", f"Pet ID '{pet_id}' does not exist.")
            return

        query = "INSERT INTO Medications (PetID, MedicationName) VALUES (%s, %s)"
        values = (pet_id, med_name)

        try:
            self.cursor.execute(query, values)
            self.db.commit()
            self.alertLabel.setText(f"Medication '{med_name}' added for Pet {pet_id}.")
            self.refreshMedTable()
        except MySQLError as err:
            QMessageBox.critical(self, "DB Error", f"Failed to add medication: {err}")
            
    def refreshMedTable(self):
        query = "SELECT PetID, MedicationName FROM Medications ORDER BY PetID"
        try:
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            
            self.medTable.setRowCount(0)
            for row, row_data in enumerate(data):
                self.medTable.insertRow(row)
                for col, value in enumerate(row_data):
                    self.medTable.setItem(row, col, QTableWidgetItem(str(value)))
        except MySQLError as err:
            QMessageBox.critical(self, "DB Error", f"Failed to refresh Medication table: {err}")

    def removeMedication(self):
        selected_rows = self.medTable.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Selection Error", "Select a medication record to remove.")
            return

        row_index = selected_rows[0].row()
        pet_id = self.medTable.item(row_index, 0).text()
        med_name = self.medTable.item(row_index, 1).text()

        query = "DELETE FROM Medications WHERE PetID = %s AND MedicationName = %s LIMIT 1"
        
        try:
            self.cursor.execute(query, (pet_id, med_name))
            self.db.commit()
            self.alertLabel.setText(f"Medication '{med_name}' removed from Pet {pet_id}.")
            self.refreshMedTable()
        except MySQLError as err:
            QMessageBox.critical(self, "DB Error", f"Failed to remove medication: {err}")


    def addVetVisit(self):
        pet_id = self.vetPetID.text().strip()
        visit_date = self.visitDate.date().toString("yyyy-MM-dd")
        notes = self.vetNotes.text().strip()

        if not pet_id or not notes:
            QMessageBox.warning(self, "Input Error", "Pet ID and Notes required.")
            return
        if not self.petExists(pet_id):
            QMessageBox.critical(self, "Input Error", f"Pet ID '{pet_id}' does not exist.")
            return

        query = "INSERT INTO VetVisits (PetID, VisitDate, Notes) VALUES (%s, %s, %s)"
        values = (pet_id, visit_date, notes)

        try:
            self.cursor.execute(query, values)
            self.db.commit()
            self.alertLabel.setText(f"Vet visit on {visit_date} recorded for Pet {pet_id}.")
            self.refreshVetTable()
        except MySQLError as err:
            QMessageBox.critical(self, "DB Error", f"Failed to add vet visit: {err}")

    def refreshVetTable(self):
        query = "SELECT PetID, VisitDate, Notes FROM VetVisits ORDER BY PetID, VisitDate DESC"
        try:
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            
            self.vetTable.setRowCount(0)
            for row, row_data in enumerate(data):
                self.vetTable.insertRow(row)
                for col, value in enumerate(row_data):
                    self.vetTable.setItem(row, col, QTableWidgetItem(str(value)))
        except MySQLError as err:
            QMessageBox.critical(self, "DB Error", f"Failed to refresh Vet Visits table: {err}")
            
    def removeVetVisit(self):
        selected_rows = self.vetTable.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Selection Error", "Select a vet visit record to remove.")
            return

        row_index = selected_rows[0].row()
        pet_id = self.vetTable.item(row_index, 0).text()
        visit_date = self.vetTable.item(row_index, 1).text()
        notes = self.vetTable.item(row_index, 2).text()

        query = "DELETE FROM VetVisits WHERE PetID = %s AND VisitDate = %s AND Notes = %s LIMIT 1"
        
        try:
            self.cursor.execute(query, (pet_id, visit_date, notes))
            self.db.commit()
            self.alertLabel.setText(f"Vet visit on {visit_date} removed from Pet {pet_id}.")
            self.refreshVetTable()
        except MySQLError as err:
            QMessageBox.critical(self, "DB Error", f"Failed to remove vet visit: {err}")

    def addVaccination(self):
        pet_id = self.vacPetID.text().strip()
        vac_name = self.vacName.text().strip()
        vac_date = self.vacDate.date().toString("yyyy-MM-dd")

        if not pet_id or not vac_name:
            QMessageBox.warning(self, "Input Error", "Pet ID and Vaccine Name required.")
            return
        if not self.petExists(pet_id):
            QMessageBox.critical(self, "Input Error", f"Pet ID '{pet_id}' does not exist.")
            return

        query = "INSERT INTO Vaccinations (PetID, VaccineName, DateGiven) VALUES (%s, %s, %s)"
        values = (pet_id, vac_name, vac_date)

        try:
            self.cursor.execute(query, values)
            self.db.commit()
            self.alertLabel.setText(f"Vaccination '{vac_name}' recorded for Pet {pet_id}.")
            self.refreshVacTable()
        except MySQLError as err:
            QMessageBox.critical(self, "DB Error", f"Failed to add vaccination: {err}")

    def removeVaccination(self):
        selected_rows = self.vacTable.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Selection Error", "Select a vaccination record to remove.")
            return

        row_index = selected_rows[0].row()
        pet_id = self.vacTable.item(row_index, 0).text()
        vac_name = self.vacTable.item(row_index, 1).text()
        vac_date = self.vacTable.item(row_index, 2).text() 

        query = "DELETE FROM Vaccinations WHERE PetID = %s AND VaccineName = %s AND DateGiven = %s LIMIT 1"
        
        try:
            self.cursor.execute(query, (pet_id, vac_name, vac_date))
            self.db.commit()
            self.alertLabel.setText(f"Vaccination '{vac_name}' removed from Pet {pet_id}.")
            self.refreshVacTable()
        except MySQLError as err:
            QMessageBox.critical(self, "DB Error", f"Failed to remove vaccination: {err}")

    def refreshVacTable(self):
        query = "SELECT PetID, VaccineName, DateGiven FROM Vaccinations ORDER BY PetID, DateGiven DESC"
        try:
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            
            self.vacTable.setRowCount(0)
            for row, row_data in enumerate(data):
                self.vacTable.insertRow(row)
                for col, value in enumerate(row_data):
                    self.vacTable.setItem(row, col, QTableWidgetItem(str(value)))
        except MySQLError as err:
            QMessageBox.critical(self, "DB Error", f"Failed to refresh Vaccinations table: {err}")
            
    def generateReport(self):
        pet_id = self.diagPetID.text().strip()

        if not pet_id:
            self.reportOutput.setHtml("<p style='color:red;'><b>Error:</b> Please enter a Pet ID.</p>")
            return
        
        try:
            self.cursor.execute("SELECT Name, Type, Breed FROM Pets WHERE PetID = %s", (pet_id,))
            pet_info = self.cursor.fetchone()
            
            if not pet_info:
                self.reportOutput.setHtml(f"<p style='color:red;'><b>Error:</b> Pet ID <b>{pet_id}</b> not found.</p>")
                return
            
            name, pet_type, breed = pet_info
            
            report_html = f"<h2>Health Report for {name}</h2>"
            report_html += f"<p><b>Type:</b> {pet_type}, <b>Breed:</b> {breed}</p><hr>"
            
            report_html += "<h3> Medication History</h3>"
            self.cursor.execute("SELECT MedicationName FROM Medications WHERE PetID = %s ORDER BY MedicationName", (pet_id,))
            meds = self.cursor.fetchall()
            if meds:
                report_html += "<ul>"
                for (med,) in meds:
                    report_html += f"<li>{med}</li>"
                report_html += "</ul>"
            else:
                report_html += "<p><i>No medications recorded.</i></p>"
                
            report_html += "<h3>Vaccination History</h3>"
            self.cursor.execute("SELECT VaccineName, DateGiven FROM Vaccinations WHERE PetID = %s ORDER BY DateGiven DESC", (pet_id,))
            vax = self.cursor.fetchall()
            if vax:
                report_html += "<table border='1' cellpadding='5' cellspacing='0' style='border-collapse: collapse; width: 100%; font-size: 10pt;'>"
                report_html += "<tr><th style='background-color:#f9b8c7;'>Vaccine</th><th style='background-color:#f9b8c7;'>Date Given</th></tr>"
                for vaccine, date in vax:
                    report_html += f"<tr><td>{vaccine}</td><td>{date.strftime('%Y-%m-%d')}</td></tr>"
                report_html += "</table>"
            else:
                report_html += "<p><i>No vaccinations recorded.</i></p>"
                
            report_html += "<h3>Vet Visit History & Treatment Plan</h3>"
            self.cursor.execute("SELECT VisitDate, Notes FROM VetVisits WHERE PetID = %s ORDER BY VisitDate DESC", (pet_id,))
            visits = self.cursor.fetchall()
            if visits:
                for date, notes in visits:
                    formatted_notes = notes.replace('\n', '<br>')
                    report_html += f"<p><b>Date: {date.strftime('%Y-%m-%d')}</b></p>"
                    report_html += f"<div style='border-left: 3px solid #f08095; padding: 5px 10px; margin-bottom: 10px; background-color: #fff4f6; border-radius: 5px;'>{formatted_notes}</div>"
            else:
                report_html += "<p><i>No vet visits recorded.</i></p>"

            self.reportOutput.setHtml(report_html)

        except MySQLError as err:
            self.reportOutput.setHtml(f"<p style='color:red;'><b>Database Error:</b> Failed to generate report. {err}</p>")
        except Exception as e:
            self.reportOutput.setHtml(f"<p style='color:red;'><b>General Error:</b> {e}</p>")
            
    def searchPet(self):
        search_text = self.searchBox.text().strip()
        
        if not search_text:
            self.refreshTable()
            self.alertLabel.setText("Showing all pets.")
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
        pet_id = self.petTable.item(row, 0).text()
        self.petID.setText(pet_id)
        self.petName.setText(self.petTable.item(row, 1).text())
        self.petType.setText(self.petTable.item(row, 2).text())
        self.petBreed.setText(self.petTable.item(row, 3).text())
        
        self.updateSubTabPetIDs(pet_id)