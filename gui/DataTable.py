from database import *
import Wizard
from PyQt5 import QtWidgets, QtGui, QtCore
import json


class DataTable(QtWidgets.QTableWidget):
    def __init__(self, parent: QtWidgets.QMainWindow, database: DatabaseInterface, icon: QtGui.QIcon):
        super().__init__()
        DIAGNOSIS_COL_IDX = 6
        self.mainWindow = parent
        self.database = database
        self.latestPatientId = -1
        self.contextMenu = QtWidgets.QMenu()
        self.updateAction = QtWidgets.QAction("Edit patient record")
        self.updateAction.triggered.connect(self._onPatientUpdateTriggered)
        self.deletePatient = QtWidgets.QAction("Delete patient record")
        self.deletePatient.triggered.connect(self._onDeletePatientTriggered)
        self.contextMenu.addAction(self.updateAction)
        self.contextMenu.addAction(self.deletePatient)

        self.setRowCount(0)
        self.setColumnCount(9)  # TODO: 10 in case the diagnostic data is included
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setHorizontalHeaderLabels(["Patient ID", "Name", "Surname", "Age", "PESEL",
                                                    "Gender",
                                                    "Diagnosis",
                                                    # "Diagnostic data", # TODO: for now skip diagnostic data
                                                    "Audio signals",
                                                    "Timestamp"])
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setDefaultSectionSize(150)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        self.horizontalHeader().setSectionResizeMode(DIAGNOSIS_COL_IDX, QtWidgets.QHeaderView.Interactive)
        self.cellDoubleClicked.connect(self._onCellDoubleClicked)

        self.diagnosticMessage = QtWidgets.QMessageBox(parent)
        self.icon = icon
        self.diagnosticMessage.setWindowIcon(self.icon)
        self.diagnosticMessage.setWindowTitle("TMJ RDC Diagnosis")
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._handleContextMenu)

    def loadDatabase(self):
        self.setRowCount(0)
        databaseData = self.database.getData()
        if len(databaseData) == 0:
            self._emptyDatabaseNotification()
        for rowIdx, rowData in enumerate(databaseData):
            visibleData, timestamp = self._excludeNonVisibleDataFromRecord(list(rowData))
            self.insertRow(rowIdx)
            for columnIdx, data in enumerate(visibleData):
                self.setItem(rowIdx, columnIdx, QtWidgets.QTableWidgetItem(str(data)))
            self.setItem(rowIdx, columnIdx+1, QtWidgets.QTableWidgetItem("AUDIO"))
            self.setItem(rowIdx, columnIdx+2, QtWidgets.QTableWidgetItem(str(timestamp)))

    @staticmethod
    def _excludeNonVisibleDataFromRecord(patientRecord: list) -> tuple:
        timestamp = patientRecord[-1]
        diagnosis = patientRecord[7]
        visibleData = patientRecord[0:6]
        visibleData.append(diagnosis)
        return visibleData, timestamp

    def _emptyDatabaseNotification(self):
        message = QtWidgets.QMessageBox(self)
        message.setWindowIcon(self.icon)
        message.setWindowTitle("Info")
        message.setText("Empty database")
        message.exec_()

    def _onCellDoubleClicked(self, row: int, column: int):
        columnName = self.horizontalHeaderItem(column).text()
        if columnName == "Diagnosis":
            diagnosis = self.item(row, column).text()
            self.diagnosticMessage.setText(self._formatDiagnosis(diagnosis))
            self.diagnosticMessage.exec_()
        elif columnName == "Audio signals":
            pass # TODO: implement signals visualization

    def _handleContextMenu(self, pos: QtCore.QPoint):
        item = self.itemAt(pos)
        if item:
            PATIENT_ID_COL = 0
            patientIdItem = self.item(item.row(), PATIENT_ID_COL)
            if patientIdItem:
                self.latestPatientId = patientIdItem.text()
                self.contextMenu.popup(self.viewport().mapToGlobal(pos))

    def _onPatientUpdateTriggered(self):
        self.mainWindow.getWizard().open(action=Wizard.UPDATE, patientId=self.latestPatientId)

    def _onDeletePatientTriggered(self):
        self.database.removeRecordOnId(self.latestPatientId)
        self.loadDatabase()

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
