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


class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("TMJ RDC Diagnoser")
        self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))
        self.path = ""

        quitAction = QAction("Open", self)
        quitAction.setShortcut("Ctrl+O")
        quitAction.setStatusTip('Open the examination file')
        quitAction.triggered.connect(self.openDiagnosticFile)

        openAction = QAction("Quit", self)
        openAction.setShortcut("Ctrl+Q")
        openAction.setStatusTip('Quit the application')
        openAction.triggered.connect(QtWidgets.QApplication.quit)

        generateDiagnosisAction = QAction("Generate diagnostic file", self)
        generateDiagnosisAction.setStatusTip('Generate the diagnosis based on the the examination file')
        generateDiagnosisAction.triggered.connect(self.generateDiagnosticReport)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        fileMenu.addAction(quitAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(generateDiagnosisAction)

        self.show()

    # handle close button of the main window (quit QApplication properly)
    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Window close", "Close the Diagnoser?",
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if (reply == QMessageBox.Yes):
            event.accept()
            QtWidgets.QApplication.quit()
        else:
            event.ignore()

    def openDiagnosticFile(self):
        fileName, fileFilter = QFileDialog.getOpenFileName(self, 'Open File',
                                               filter="Excel files (*.xlsx)")

        try:
            # Import datasets as separate spreadsheets
            axis1_sheet = pd.read_excel(fileName, sheet_name = 'axis I')
            palpation_sheet = pd.read_excel(fileName, sheet_name = 'axis I palpacja')
            q_sheet = pd.read_excel(fileName, sheet_name = 'Q')

            # transform to np objects
            axis1_data = removeEmpty(axis1_sheet.to_numpy())
            palpation_data = removeEmpty(palpation_sheet.to_numpy())
            q_data = removeEmpty(q_sheet.to_numpy())

            # assume that all sheets have the same number of records/patients
            assert(len(axis1_data) == len(palpation_data) == len(q_data))

            persons, axisOnes, palpations, qs = parseDatabase(axis1_data, palpation_data, q_data)
            patients = formPatientsDict(persons, axisOnes, palpations, qs)
            self.patients = patients
            QMessageBox.question(self, "TMJ RDC Diagnoser", "File loaded properly",
                                 QMessageBox.Ok, QMessageBox.Ok)
            printDiagnosis(patients)
        except:
            QMessageBox.question(self, "TMJ RDC Diagnoser", "Wrong file format!",
                     QMessageBox.Ok, QMessageBox.Ok)

    def generateDiagnosticReport(self):
        # TODO: implement
        pass

def run():
        app = QtWidgets.QApplication(sys.argv)
        window = Window()
        app.exec_()

if __name__ == "__main__":
    run()
