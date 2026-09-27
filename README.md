# Pet Health Management System (PHMS)

A desktop-based Pet Health Management System built with Python, PyQt6, and MySQL. The system provides an interactive graphical interface to manage and track pet profiles, medical visits, vaccinations, and medication records.

---

## Features

- **Authentication:** Secure login interface for system access.
- **Pet Records:** Register and manage pet profiles and ownership details.
- **Medical & Treatment Logs:** Track veterinarian visits, diagnoses, and medical histories.
- **Medications & Vaccinations:** Monitor prescribed medications and upcoming or administered vaccine schedules.
- **Relational Database Backend:** Persistent, structured data storage using MySQL.

---

## Database Architecture

The system connects to a relational MySQL database containing four core entities:
- **`Pets`**: Stores pet profiles and identifiers.
- **`Medication`**: Manages prescription records, dosages, and administration details.
- **`Vet Visit History`**: Logs clinic visits, veterinarian consultations, and visit outcomes.
- **`Vaccination`**: Tracks vaccination dates, vaccine types, and renewal schedules.

---

## Project Structure

```text
PHMS/
│
├── app.py                 # Main entry point of the application
├── loginwindow.py         # Login controller and logic
├── loginwindow.ui         # Qt Designer UI layout for the login window
├── ui_loginwindow.py      # Compiled PyQt6 code for login window
│
├── mainwindow.py          # Main dashboard controller and business logic
├── mainwindow.ui          # Qt Designer UI layout for the main application window
├── ui_mainwindow.py       # Compiled PyQt6 code for main window
│
└── README.md              # Project documentation
```
