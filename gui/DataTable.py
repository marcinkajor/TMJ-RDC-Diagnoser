from database import *
from PyQt5 import QtWidgets, QtGui, QtCore
import json


class DataTable(QtWidgets.QTableWidget):
    def __init__(self, parent: QtWidgets.QMainWindow, database: DatabaseInterface, icon: QtGui.QIcon):
        super().__init__()
        DIAGNOSIS_COL_IDX = 6
        self.database = database
        self.setRowCount(0)
        self.setColumnCount(8)  # TODO: 9 in case the diagnostic data is included
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setHorizontalHeaderLabels(["Patient ID", "Name", "Surname", "Age", "PESEL",
                                                    "Gender",
                                                    "Diagnosis",
                                                    # "Diagnostic data", # TODO: for now skip diagnostic data
                                                    "Timestamp"])
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setDefaultSectionSize(150)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        self.horizontalHeader().setSectionResizeMode(DIAGNOSIS_COL_IDX, QtWidgets.QHeaderView.Interactive)
        self.cellDoubleClicked.connect(self._onCellDoubleClicked)

        self.diagnosticMessage = QtWidgets.QMessageBox(parent)
        self.diagnosticMessage.setWindowIcon(icon)
        self.diagnosticMessage.setWindowTitle("TMJ RDC Diagnosis")
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._handleContextMenu)

    def loadDatabase(self):
        self.setRowCount(0)
        databaseData = self.database.getData()
        if len(databaseData) == 0:
            self._emptyDatabaseNotification()
        for rowIdx, rowData in enumerate(databaseData):
            rowData = list(rowData)
            # TODO: this is to exclude diagnostic data
            del(rowData[6])
            #
            self.insertRow(rowIdx)
            for columnIdx, data in enumerate(rowData):
                self.setItem(rowIdx, columnIdx, QtWidgets.QTableWidgetItem(str(data)))

    def _emptyDatabaseNotification(self):
        message = QtWidgets.QMessageBox(self)
        message.setWindowIcon(self.icon)
        message.setWindowTitle("Info")
        message.setText("Empty database")
        message.exec_()

    def _onCellDoubleClicked(self, row: int, column: int):
        if self.horizontalHeaderItem(column).text() == "Diagnosis":
            diagnosis = self.item(row, column).text()
            self.diagnosticMessage.setText(self._formatDiagnosis(diagnosis))
            self.diagnosticMessage.exec_()
        else:  # Only show diagnosis
            pass

    def _handleContextMenu(self, pos: QtCore.QPoint):
        item = self.itemAt(pos)
        if item:
            # TODO: implement a possibility of modification of patient record
            print(item.text())

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
