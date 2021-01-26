# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 23:01:01 2020

@author: Marcin
"""

from PyQt5.QtWidgets import QWizard
from PyQt5.QtGui import QIcon
from gui.wizard_pages import *


class Wizard(QWizard):
    def __init__(self, database):
        super().__init__()
        self.database = database
        self.button(QWizard.NextButton).clicked.connect(self._onNextCLicked)
        self.button(QWizard.FinishButton).clicked.connect(self._onFinishedClicked)
        self.setWindowTitle("Add patient record")
        self.setWizardStyle(QWizard.ModernStyle)
        self.setWindowIcon(QIcon('../tooth.png'))
        # TODO: find out why only Watermark works here! Banner and Logo not working
        # self.setPixmap(QWizard.WatermarkPixmap, QPixmap('steth.png'))
        # TODO: add all necessary pages
        self.addPage(PersonalDataPage())
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
        self.addPage(DiagnosisPage())

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
            self.database.storePatientRecord(self.getParametersMap())
        except Exception as e:
            print(e)
        self._clearAllPages()
        self.restart()
