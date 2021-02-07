from PyQt5 import QtWidgets, QtGui
import sys
import pandas as pd
from algo.AlgoHelpers import removeEmpty, printDiagnosis
from algo.AlgoPatient import formPatientsDict
from algo.AlgoParser import parseDatabase
from algo.Diagnoser import Diagnoser
from algo.DatabaseDeserializer import DatabaseDeserializer
from algo.DatabaseMapper import DatabaseRecordMapper
import csv
import os
import ctypes
from gui.Wizard import Wizard
import json
from database import *

# needed for custom toolbar icon
# https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105
if os.name == 'nt':  # 'nt' - Windows, 'posix' - Linux
    myappid = u'tmj-diagnoser'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


class Window(QtWidgets.QMainWindow):
    def __init__(self, database: DatabaseInterface):
        super().__init__()

        self.database = database
        self.database.connect()
        self.database.createPatientTable('patients')

        self.diagnoser = Diagnoser(DatabaseRecordMapper(), DatabaseDeserializer(self.database))

        self.setGeometry(500, 150, 1000, 800)
        self.setWindowTitle("TMJ RDC Diagnoser")
        self.icon = QtGui.QIcon('../tooth.png')
        self.setWindowIcon(self.icon)
        self.path = ""

        self.centralWidget = QtWidgets.QWidget()
        self.centralLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.setCentralWidget(self.centralWidget)

        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(8)  # TODO: 9 in case the diagnostic data is included
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setHorizontalHeaderLabels(["Patient ID", "Name", "Surname", "Age", "PESEL",
                                                    "Gender",
                                                    "Diagnosis",
                                                    # "Diagnostic data", # TODO: for now skip diagnostic data
                                                    "Timestamp"])
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(150)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        DIAGNOSIS_COL_IDX = 6
        self.tableWidget.horizontalHeader().setSectionResizeMode(DIAGNOSIS_COL_IDX, QtWidgets.QHeaderView.Interactive)
        self.tableWidget.cellDoubleClicked.connect(self._onCellDoubleClicked)
        self.centralLayout.addWidget(self.tableWidget)

        self.diagnosticMessage = QtWidgets.QMessageBox(self)
        self.diagnosticMessage.setWindowIcon(self.icon)
        self.diagnosticMessage.setWindowTitle("TMJ RDC Diagnosis")

        openAction = QtWidgets.QAction("Open", self)
        openAction.setShortcut("Ctrl+O")
        openAction.setStatusTip('Open the examination file')
        openAction.triggered.connect(self._openDiagnosticFile)

        addRecord = QtWidgets.QAction("Add patient record", self)
        addRecord.setShortcut("Ctrl+p")
        addRecord.setStatusTip('Add patient record')
        addRecord.triggered.connect(self.addPatientRecord)

        quitAction = QtWidgets.QAction("Quit", self)
        quitAction.setShortcut("Ctrl+Q")
        quitAction.setStatusTip('Quit the application')
        quitAction.triggered.connect(QtWidgets.QApplication.quit)

        generateDiagnosisAction = QtWidgets.QAction("Generate diagnostic file", self)
        generateDiagnosisAction.setStatusTip('Generate the diagnosis based on the the examination file')
        generateDiagnosisAction.triggered.connect(self._generateDiagnosticReport)

        parsePatientRecord = QtWidgets.QAction("Show database", self)
        parsePatientRecord.setShortcut("Ctrl+l")
        parsePatientRecord.setStatusTip('Load patient database')
        parsePatientRecord.triggered.connect(self._loadDatabase)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        fileMenu.addAction(quitAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(generateDiagnosisAction)
        fileMenu.addAction(addRecord)
        fileMenu.addAction(parsePatientRecord)

        # TODO: avoid duplicating the database in the Wizard (Diagnoser already have it)
        # maybe the Diagnoser shall not use the database object at all
        self.navigator = Wizard(self.database, self.diagnoser)

        self.show()

    def addPatientRecord(self):
        self.navigator.open()

    # handle close button of the main window (quit QApplication properly)
    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, "Window close", "Close the Diagnoser?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            QtWidgets.QApplication.quit()
        else:
            event.ignore()

    def _openDiagnosticFile(self):
        fileName, fileFilter = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File',
                                                           filter="Excel files (*.xls)")
        try:
            # Import datasets as separate spreadsheets
            axis1_sheet = pd.read_excel(fileName, sheet_name='axis I')
            palpation_sheet = pd.read_excel(fileName, sheet_name='axis I palpacja')
            q_sheet = pd.read_excel(fileName, sheet_name='Q')

            # transform to np objects
            axis1_data = removeEmpty(axis1_sheet.to_numpy())
            palpation_data = removeEmpty(palpation_sheet.to_numpy())
            q_data = removeEmpty(q_sheet.to_numpy())

            # assume that all sheets have the same number of records/patients
            assert (len(axis1_data) == len(palpation_data) == len(q_data))

            persons, axisOnes, palpations, qs = parseDatabase(axis1_data, palpation_data, q_data)
            patients = formPatientsDict(persons, axisOnes, palpations, qs)
            self.patients = patients
            QtWidgets.QMessageBox.question(self, "TMJ RDC Diagnoser", "File loaded properly",
                                           QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
            printDiagnosis(patients)
        except Exception as e:
            print(e)
            QtWidgets.QMessageBox.question(self, "TMJ RDC Diagnoser", "Wrong file format!",
                                           QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)

    def _generateDiagnosticReport(self):
        path, fileFilter = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file',
                                                       filter="Excel file (*.xlsx) ;; CSV (*.csv)")

        filename, fileExtension = os.path.splitext(path)
        if fileExtension == ".csv":
            self._saveDataToCsv(path)
        elif fileExtension == ".xlsx":
            try:
                self._saveDataToXlsx(path)
            except Exception as e:
                print(e)

    def _saveDataToCsv(self, path):
        with open(path, mode='w', newline='') as file:
            fileWriter = csv.writer(file, delimiter=',')
            fileWriter.writerow(['Id', 'Name', 'Surname', 'Axis I1', 'Axis I2 left',
                                 'Axis I2 right', 'Axis I3 left', 'Axis I3 right'])
            for patient in self.patients:
                idx = patient.idx
                name = patient.personalData.name
                surname = patient.personalData.surname
                diag11 = patient.getAxisI1Diagnosis()
                diag12left = patient.getAxisI2Diagnosis("left")
                diag12right = patient.getAxisI2Diagnosis("right")
                diag13left = patient.getAxisI3Diagnosis("left")
                diag13right = patient.getAxisI3Diagnosis("right")
                fileWriter.writerow([idx, name, surname, diag11, diag12left,
                                     diag12right, diag13left, diag13right])

    def _saveDataToXlsx(self, path):
        data = []
        for patient in self.patients:
            idx = patient.idx
            name = patient.personalData.name
            surname = patient.personalData.surname
            diag11 = patient.getAxisI1Diagnosis()
            diag12left = patient.getAxisI2Diagnosis("left")
            diag12right = patient.getAxisI2Diagnosis("right")
            diag13left = patient.getAxisI3Diagnosis("left")
            diag13right = patient.getAxisI3Diagnosis("right")
            data.append([idx, name, surname, diag11, diag12left,
                         diag12right, diag13left, diag13right])

        df = pd.DataFrame(data, columns=['Id', 'Name', 'Surname', 'Axis I1', 'Axis I2 left',
                                         'Axis I2 right', 'Axis I3 left', 'Axis I3 right'])
        writer = pd.ExcelWriter(path)
        df.to_excel(writer, sheet_name='Diagnosis', index=False)
        writer.save()

    def _loadDatabase(self):
        self.tableWidget.setRowCount(0)
        databaseData = self.database.getData()
        if len(databaseData) == 0:
            self._emptyDatabaseNotification()
        for rowIdx, rowData in enumerate(databaseData):
            rowData = list(rowData)
            # TODO: this is to exclude diagnostic data
            del(rowData[6])
            #
            self.tableWidget.insertRow(rowIdx)
            for columnIdx, data in enumerate(rowData):
                self.tableWidget.setItem(rowIdx, columnIdx, QtWidgets.QTableWidgetItem(str(data)))

    def _emptyDatabaseNotification(self):
        message = QtWidgets.QMessageBox(self)
        message.setWindowIcon(self.icon)
        message.setWindowTitle("Info")
        message.setText("Empty database")
        message.exec_()

    def _onCellDoubleClicked(self, row: int, column: int):
        if self.tableWidget.horizontalHeaderItem(column).text() == "Diagnosis":
            diagnosis = self.tableWidget.item(row, column).text()
            self.diagnosticMessage.setText(self._formatDiagnosis(diagnosis))
            self.diagnosticMessage.exec_()
        else:  # Only show diagnosis
            pass

    @staticmethod
    def _formatDiagnosis(jsonString: str) -> str:
        outputFormat = '''<pre>
                          <p>Axis I: Group I:<strong> {}</strong></p>
                          <p>Axis I: Group II:</p>
                          <p>  Right: <strong> {}</strong></p>
                          <p>  Left:  <strong> {}</strong></p>
                          <p>Axis I: Group III:</p>
                          <p>  Right: <strong> {}</strong></p>
                          <p>  Left:  <strong> {}</strong></p>'''
        try:
            diagnosticMap = json.loads(jsonString)
            values = diagnosticMap.values()
            return outputFormat.format(*values)
        except Exception as e:
            print(str(e))
            return None


def run():
    app = QtWidgets.QApplication(sys.argv)
    window = Window(DatabaseSQLite('patients_database'))
    app.exec_()


if __name__ == "__main__":
    run()
