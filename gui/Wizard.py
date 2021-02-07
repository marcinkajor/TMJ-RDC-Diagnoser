# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 23:01:01 2020

@author: Marcin
"""

from PyQt5.QtWidgets import QWizard
from PyQt5.QtGui import QIcon, QCloseEvent
from algo.Diagnoser import Diagnoser
from gui.wizard_pages import *
from gui.DataTable import DataTable


class Wizard(QWizard):
    def __init__(self, database, diagnoser: Diagnoser, dataTable: DataTable):
        super().__init__()
        self.database = database
        self.diagoser = diagnoser
        self.dataTable = dataTable
        self.button(QWizard.NextButton).clicked.connect(self._onNextCLicked)
        self.button(QWizard.FinishButton).clicked.connect(self._onFinishedClicked)
        self.button(QWizard.CancelButton).clicked.connect(self._onCancelClicked)
        self.setWindowTitle("Add patient record")
        self.setWizardStyle(QWizard.ModernStyle)
        self.setWindowIcon(QIcon('../tooth.png'))
        # TODO: find out why only Watermark works here! Banner and Logo not working
        # self.setPixmap(QWizard.WatermarkPixmap, QPixmap('steth.png'))
        # TODO: add all necessary pages
        self.addPage(PersonalDataPage())
        self.addPage(QuestionnairePage())
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
            diagnosis = {"Axis11": axis11, "Axis12Right": axis12r, "Axis12Left": axis12l,
                         "Axis13Right": axis13r, "Axis13Left": axis13l}
            patientRecord["Diagnosis"] = diagnosis
            self.database.storePatientRecord(patientRecord)
            self.dataTable.loadDatabase()
        except Exception as e:
            self.database.storePatientRecord(self.getParametersMap())
            print(e)
        self._clearAllPages()
        self.restart()

    def _onCancelClicked(self):
        self._clearAllPages()
        self.restart()

    def closeEvent(self, event: QCloseEvent):
        self._onCancelClicked()
        event.accept()
