from PyQt5 import QtWidgets, QtGui
import sys
import pandas as pd
from algo.AlgoHelpers import removeEmpty, printDiagnosis
from algo.AlgoPatient import formPatientsDict
from algo.AlgoParser import parseDatabase
from algo.Diagnoser import Diagnoser
from algo.DatabaseDeserializer import DatabaseDeserializer
from algo.DatabaseMapper import DatabaseRecordMapper
from gui.DataTable import DataTable
import csv
import os
import ctypes
from gui.Wizard import Wizard
from database import *
from Statistics.Stats import Stats
from gui.StatsWidget import StatsWidget
from audio.AudioHandler import AudioSerializer, AudioManager
from zipfile import ZipFile
import json
import shutil


# needed for custom toolbar icon
# https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105
if os.name == 'nt':  # 'nt' - Windows, 'posix' - Linux
    myappid = u'tmj-diagnoser'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

DATABASE_NAME = "patients_database"


class Window(QtWidgets.QMainWindow):
    def __init__(self, database: DatabaseInterface):
        super().__init__()

        self.database = database
        self.database.connect()
        self.database.createPatientTable('patients')
        self.statistics = Stats(self.database)

        self.diagnoser = Diagnoser(DatabaseRecordMapper(), DatabaseDeserializer(self.database))

        self.setGeometry(500, 150, 1000, 800)
        self.setWindowTitle("TMJ RDC Diagnoser")
        self.icon = QtGui.QIcon('../tooth.png')
        self.setWindowIcon(self.icon)
        self.path = ""

        self.centralWidget = QtWidgets.QWidget()
        self.centralLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.setCentralWidget(self.centralWidget)

        self.table = DataTable(self,  self.database, self.icon)
        self.centralLayout.addWidget(self.table)

        self.statistics = Stats(self.database)
        self.statsTabWidget = StatsWidget(self.statistics, self.icon)
        self.statsTabWidget.setWindowTitle("Database statistics")
        self.database.changed.connect(self.statsTabWidget.update)

        openAction = QtWidgets.QAction("Open", self)
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

        showDatabase = QtWidgets.QAction("Show database", self)
        showDatabase.setShortcut("Ctrl+l")
        showDatabase.setStatusTip('Load patient database')
        showDatabase.triggered.connect(self.table.loadDatabase)

        exportDatabase = QtWidgets.QAction("Export database", self)
        exportDatabase.setShortcut("Ctrl+e")
        exportDatabase.setStatusTip('Export database to the file')
        exportDatabase.triggered.connect(self._exportDatabase)

        importDatabase = QtWidgets.QAction("Import database", self)
        importDatabase.setShortcut("Ctrl+i")
        importDatabase.setStatusTip('Import database from the file')
        importDatabase.triggered.connect(self._importDatabase)

        showStats = QtWidgets.QAction("Show statistics", self)
        showStats.setShortcut("Ctrl+s")
        showStats.setStatusTip('Show database diagnosis statistics')
        showStats.triggered.connect(lambda: self.statsTabWidget.show())

        exportAudioFiles = QtWidgets.QAction("Export audio files", self)
        exportAudioFiles.setShortcut("Ctrl+a")
        exportAudioFiles.setStatusTip("Exports all WAV files together with RDC diagnosis to the archive")
        exportAudioFiles.triggered.connect(self._exportAudio)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        fileMenu.addAction(quitAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(generateDiagnosisAction)
        fileMenu.addAction(addRecord)
        fileMenu.addAction(showDatabase)
        fileMenu.addAction(exportDatabase)
        fileMenu.addAction(importDatabase)
        fileMenu.addAction(showStats)
        fileMenu.addAction(exportAudioFiles)

        # TODO: avoid duplicating the database in the Wizard (Diagnoser already have it)
        # maybe the Diagnoser shall not use the database object at all
        self.wizard = Wizard(self.database, self.diagnoser, self.table)
        self.wizard.isDone.connect(lambda: self.setEnabled(True))
        self.show()

    def getWizard(self) -> Wizard:
        return self.wizard

    def addPatientRecord(self):
        self.wizard.open()
        self.setEnabled(False)

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
        fileName, fileFilter = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', filter="Excel files (*.xls)")
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

    def _exportDatabase(self):
        path, fileFilter = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', filter="RDC database(*.rdc)")
        self._swapFiles('../' + DATABASE_NAME + '.db', path)

    def _swapFiles(self, sourceFileName: str, targetFileName: str):
        try:
            with open(sourceFileName, mode='rb') as sourceFile:
                content = sourceFile.read()
                with open(targetFileName, mode='wb') as targetFile:
                    targetFile.write(content)
        except Exception as e:
            print(e)
            self._showErrorNotification(str(e))

    def _showErrorNotification(self, msgText: str):
        message = QtWidgets.QMessageBox(self)
        message.setIcon(QtWidgets.QMessageBox.Critical)
        message.setWindowTitle("Error")
        message.setText(msgText)
        message.exec_()

    def _importDatabase(self):
        fileName, fileFilter = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File',
                                                                     filter="RDC database file (*.rdc)")
        self._swapFiles(fileName, '../' + DATABASE_NAME + '.db')
        self.table.loadDatabase()
        self.statsTabWidget.update()

    def _exportAudio(self):
        path, fileFilter = QtWidgets.QFileDialog.getSaveFileName(self, 'Export audio files',
                                                                 filter="(*.zip)")
        databaseName = "tmj_sound_database"
        diagnosisColumn = 7
        dirPath = os.path.join(os.path.dirname(path), databaseName)
        audioSerializer = AudioSerializer(self, self.icon)
        ids = self.database.getPatientIds()
        counter = 0
        for patientId in ids:
            record = self.database.getPatientRecordById(patientId)
            audioFiles = DataTable.getNonEmptyAudioItems(record)
            patientDir = os.path.join(dirPath, str(patientId))
            if audioFiles:
                try:
                    os.makedirs(patientDir)
                except FileExistsError:
                    pass
                for audio in audioFiles:
                    counter += 1
                    name = audio[0]
                    fs, signal = AudioManager.parseWavFile(audio[1])
                    audioSerializer.serialize(os.path.join(patientDir, name), fs, signal)
                with open(os.path.join(patientDir, "diagnosis.json"), 'w') as jsonFile:
                    diagnosis = record[diagnosisColumn]
                    try:
                        json.dump(diagnosis, jsonFile, ensure_ascii=False, indent=4)
                    except Exception as e:
                        print(e)
        print("Audio files count: {}".format(counter))
        shutil.make_archive(path, 'zip', dirPath)
        shutil.rmtree(dirPath, ignore_errors=True)


def run():
    app = QtWidgets.QApplication(sys.argv)
    window = Window(DatabaseSQLite(DATABASE_NAME))
    app.exec_()


if __name__ == "__main__":
    run()
