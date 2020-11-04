# -*- coding: utf-8 -*-
"""
Created on Tue May  5 19:49:43 2020

@author: Marcin
"""

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QAction, QFileDialog
import sys
import pandas as pd
from qhelpers import removeEmpty, printDiagnosis
from qpatient import formPatientsDict
from qparser import parseDatabase
import csv
import os
import ctypes
from qnavigator import Navigator
from qdb import Database

# needed for custom toolbar icon
# https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105
if os.name == 'nt':  # 'nt' - Windows, 'posix' - Linux
    myappid = u'tmj-diagnoser'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.database = Database()
        self.database.connect()
        self.database.createPatientTable()

        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("TMJ RDC Diagnoser")
        self.setWindowIcon(QtGui.QIcon('tooth.png'))
        self.path = ""

        openAction = QAction("Open", self)
        openAction.setShortcut("Ctrl+O")
        openAction.setStatusTip('Open the examination file')
        openAction.triggered.connect(self._openDiagnosticFile)

        addRecord = QAction("Add patient record", self)
        addRecord.setShortcut("Ctrl+p")
        addRecord.setStatusTip('Add patient record')
        addRecord.triggered.connect(self.addPatientRecord)

        quitAction = QAction("Quit", self)
        quitAction.setShortcut("Ctrl+Q")
        quitAction.setStatusTip('Quit the application')
        quitAction.triggered.connect(QtWidgets.QApplication.quit)

        generateDiagnosisAction = QAction("Generate diagnostic file", self)
        generateDiagnosisAction.setStatusTip('Generate the diagnosis based on the the examination file')
        generateDiagnosisAction.triggered.connect(self._generateDiagnosticReport)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        fileMenu.addAction(quitAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(generateDiagnosisAction)
        fileMenu.addAction(addRecord)

        self.navigator = Navigator(self.database)

        self.show()

    def addPatientRecord(self):
        self.navigator.open()

    # handle close button of the main window (quit QApplication properly)
    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Window close", "Close the Diagnoser?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            QtWidgets.QApplication.quit()
        else:
            event.ignore()

    def _openDiagnosticFile(self):
        fileName, fileFilter = QFileDialog.getOpenFileName(self, 'Open File',
                                                           filter="Excel files (*.xlsx)")
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
            QMessageBox.question(self, "TMJ RDC Diagnoser", "File loaded properly",
                                 QMessageBox.Ok, QMessageBox.Ok)
            printDiagnosis(patients)
        except:
            QMessageBox.question(self, "TMJ RDC Diagnoser", "Wrong file format!",
                                 QMessageBox.Ok, QMessageBox.Ok)

    def _generateDiagnosticReport(self):
        path, fileFilter = QFileDialog.getSaveFileName(self, 'Save file',
                                                       filter="Excel file (*.xlsx) ;; CSV (*.csv)")

        filename, fileExtension = os.path.splitext(path)
        if fileExtension == ".csv":
            self._saveDataToCsv(path)
        elif fileExtension == ".xlsx":
            self._saveDataToXlsx(path)

    def _saveDataToCsv(self, path):
        with open(path, mode='w', newline='') as file:
            fileWriter = csv.writer(file, delimiter=',')
            fileWriter.writerow(['Id', 'Name', 'Surname', 'Axis I1', 'Axis I2 left',
                                 'Axis I2 right', 'Axis I3 left', 'Axis I3 right'])
            for patient in self.patients:
                idx = patient.idx
                name = patient.personalData.name
                surname = patient.personalData.surname
                diag11 = patient.getAsixI1Diagnosis()
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
            diag11 = patient.getAsixI1Diagnosis()
            diag12left = patient.getAxisI2Diagnosis("left")
            diag12right = patient.getAxisI2Diagnosis("right")
            diag13left = patient.getAxisI3Diagnosis("left")
            diag13right = patient.getAxisI3Diagnosis("right")
            data.append([idx, name, surname, diag11, diag12left,
                         diag12right, diag13left, diag13right])

        df = pd.DataFrame(data, columns=['Id', 'Name', 'Surname', 'Axis I1', 'Axis I2 left',
                                         'Axis I2 right', 'Axis I3 left', 'Axis I3 right'])
        writer = pd.ExcelWriter(path, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Diagnosis', index=False)
        # adjust the columns width
        worksheet = writer.sheets['Diagnosis']
        for idx, col in enumerate(df):
            series = df[col]
            maxLen = max((series.astype(str).map(len).max(), len(str(series.name)))) + 1
            # width is in 1 unit per font character width
            # Default font is Calibri 11px which boils down to ~8.5 pixels per unit
            worksheet.set_column(idx, idx, width=maxLen)
        writer.save()


def run():
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    app.exec_()


if __name__ == "__main__":
    run()