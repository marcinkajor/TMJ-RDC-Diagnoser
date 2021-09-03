# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 23:01:01 2020

@author: Marcin
"""

from PyQt5.QtWidgets import QWizard
from PyQt5.QtGui import QIcon, QCloseEvent, QKeyEvent
from PyQt5.QtCore import pyqtSignal, Qt
from algo.Diagnoser import Diagnoser
from gui.wizard_pages import *

STORE = 0
UPDATE = 1


class Wizard(QWizard):

    isDone = pyqtSignal()

    def __init__(self, database, diagnoser: Diagnoser, dataTable):
        super().__init__()
        self.database = database
        self.diagoser = diagnoser
        self.dataTable = dataTable
        self.action = STORE
        self.patientId = -1
        self.button(QWizard.NextButton).clicked.connect(self._onNextCLicked)
        self.button(QWizard.FinishButton).clicked.connect(self._onFinishedClicked)
        self.button(QWizard.CancelButton).clicked.connect(self._onCancelClicked)
        self.setWindowTitle("Patient record")
        self.setWizardStyle(QWizard.ModernStyle)
        self.setWindowIcon(QIcon('../tooth.png'))
        # TODO: find out why only Watermark works here! Banner and Logo not working
        # self.setPixmap(QWizard.WatermarkPixmap, QPixmap('steth.png'))
        # TODO: add all necessary pages
        self.addPage(PersonalDataPage())
        self.addPage(QuestionnairePage())
        self.addPage(Questionnaire2Page())
        self.addPage(InitialDataPage())
        self.addPage(AbductionMovementPage())
        self.addPage(VerticalMovementRangePage())
        self.addPage(IncisorsGapPage())
        self.addPage(VerticalMandibleMovementsPage())
        self.addPage(SoundsInJointAbductionPage())
        self.addPage(SoundsInJointHorizontalMovementsPage())
        self.addPage(PalpationPainNoPainPage())
        self.addPage(PalpationPainExtraoralMusclesPage())
        self.addPage(PalpationPainJointPainPage())
        self.addPage(PalpationPainIntraoralPainPage())
        self.addPage(AudioFilesPage())

    def getVisitedFieldsNames(self):
        fields = []
        for pageId in self.visitedPages():
            fields += self.page(pageId).fields
        return fields

    def getFieldsNames(self):
        fields = []
        for pageId in self.pageIds():
            fields += self.page(pageId).fields
        return fields

    def getParametersMap(self) -> dict:
        parametersMap = {}
        for name in self.getVisitedFieldsNames():
            splitName = name.split('/')
            pageName = splitName[0]
            parameterName = splitName[1]
            subMapName = pageName[:-4] if pageName.endswith('Page') else pageName
            try:
                parametersMap[subMapName][parameterName] = self.field(name)
            except KeyError:
                parametersMap[subMapName] = {}
                parametersMap[subMapName][parameterName] = self.field(name)
        return parametersMap

    def _onNextCLicked(self):
        currentPage = self.page(self.currentId() - 1)
        currentPage.onNextClicked()

    def _clearAllPages(self):
        for pageId in self.pageIds():
            try:
                self.page(pageId).clearAll()
                self.page(pageId).cleanupPage()
            except Exception as e:
                print(e)

    def _onFinishedClicked(self):
        try:
            patientRecord = self.getParametersMap()
            axis11 = self.diagoser.getPatientDiagnosisFromRecord(patientRecord, Diagnoser.DiagnosisType.AXIS_11)
            axis12r = self.diagoser.getPatientDiagnosisFromRecord(patientRecord, Diagnoser.DiagnosisType.AXIS_12_RIGHT)
            axis12l = self.diagoser.getPatientDiagnosisFromRecord(patientRecord, Diagnoser.DiagnosisType.AXIS_12_LEFT)
            axis13r = self.diagoser.getPatientDiagnosisFromRecord(patientRecord, Diagnoser.DiagnosisType.AXIS_13_RIGHT)
            axis13l = self.diagoser.getPatientDiagnosisFromRecord(patientRecord, Diagnoser.DiagnosisType.AXIS_13_LEFT)
            axis21 = self.diagoser.getPatientDiagnosisFromRecord(patientRecord, Diagnoser.DiagnosisType.AXIS_21)
            diagnosis = {"Axis11": axis11, "Axis12Right": axis12r, "Axis12Left": axis12l,
                         "Axis13Right": axis13r, "Axis13Left": axis13l, "Axis21": axis21}
            patientRecord["Diagnosis"] = diagnosis
            if self.action is STORE and self.patientId == -1:
                self.database.storePatientRecord(patientRecord)
            elif self.action is UPDATE and self.patientId != -1:
                self.database.updatePatientRecord(self.patientId, patientRecord)
            else:
                print("Unknown wizard finish action")
            self.dataTable.loadDatabase()
        except Exception as e:
            print(e)
        self._clearAllPages()
        self.restart()
        self.isDone.emit()

    def _onCancelClicked(self):
        self._clearAllPages()
        self.restart()
        self.isDone.emit()

    def _loadWithDatabaseData(self, patientId: str):
        for pageId in self.pageIds():
            try:
                self.page(pageId).loadWithData(patientId)
            except Exception as e:
                print(e)

    def closeEvent(self, event: QCloseEvent):
        self._onCancelClicked()
        event.accept()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self._onCancelClicked()
        super(Wizard, self).keyPressEvent(event)

    def open(self, action=STORE, patientId=-1):
        self.action = action
        self.patientId = patientId
        if action == UPDATE:
            self._loadWithDatabaseData(patientId)
        super().open()

    def getDatabase(self):
        return self.database
