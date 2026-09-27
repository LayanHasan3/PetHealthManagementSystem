#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QLineEdit>
#include <QPushButton>
#include <QTableWidget>
#include <QLabel>
#include <QTabWidget>
#include <QMap>
#include <QStringList>
#include <QDateEdit>
#include <QSqlDatabase> // NEW: For database connection
#include <QSqlQuery>    // NEW: For executing queries
#include <QSqlError>  
#include <QDebug>


class MainWindow : public QMainWindow {
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private:
    QWidget *centralWidget;

    // Pet info inputs
    QLineEdit *petID;
    QLineEdit *petName;
    QLineEdit *petType;
    QLineEdit *petBreed;

    // Pet management buttons
    QPushButton *addBtn;
    QPushButton *updateBtn;
    QPushButton *deleteBtn;

    // Search bar and button
    QLineEdit *searchBox;
    QPushButton *searchBtn;

    // Pet display table
    QTableWidget *petTable;

    // Informative label
    QLabel *alertLabel;

    // Tabs and medication UI
    QTabWidget *tabs;
    QWidget *medTab;
    QLineEdit *medPetID;
    QLineEdit *medName;
    QPushButton *addMedBtn;
    QPushButton *removeMedBtn;
    QTableWidget *medTable;

   // Vet Visit UI Elements
    QWidget *vetVisitTab;
    QLineEdit *vetPetID;
    QDateEdit *visitDate; 
    QLineEdit *vetNotes;
    QPushButton *addVetVisitBtn;
    QPushButton *removeVetVisitBtn;
    QTableWidget *vetTable;

    //  Vaccination UI Elements
    QWidget *vaccinationTab;
    QLineEdit *vacPetID;
    QLineEdit *vacName;
    QDateEdit *vacDate; 
    QPushButton *addVacBtn;
    QPushButton *removeVacBtn;
    QTableWidget *vacTable;

    //  Diagnosis/Report UI Elements
    QWidget *diagnosisTab;
    QLineEdit *diagPetID;
    QPushButton *generateReportBtn;
    QTextEdit *reportOutput;

     QSqlDatabase db;
    bool connectDB();
    bool petExists(const QString& petId);


    // UI setup helpers
    void setupUI();
    void setupMedTab();
    void setupVetVisitTab();
    void setupVaccinationTab();
    void setupDiagnosisTab();
    void setupConnections();
    void applyPastelTheme();

    // Data manipulation
    void addPet();
    void updatePet();
    void deletePet();
    void searchPet();

    void refreshTable();
    void refreshMedTable();
    void refreshVetTable();
    void refreshVacTable();

    void generateReport();

private slots:
    // Pet buttons
    void onAddClicked();
    void onUpdateClicked();
    void onDeleteClicked();
    void onSearchClicked();

    //med buttons
    void onAddMedicationClicked();
    void onRemoveMedicationClicked();

    // Vet Visit buttons
    void onAddVetVisitClicked();
    void onRemoveVetVisitClicked();


    // Vaccination buttons
    void onAddVaccinationClicked();
    void onRemoveVaccinationClicked();

    void onGenerateReportClicked();
};

#endif // MAINWINDOW_H
