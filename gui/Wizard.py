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

    def getFieldsNames(self):
        fields = []
        for pageId in self.visitedPages():
            fields += self.page(pageId).fields
        return fields

    def getFieldsNames(self):
        fields = []
        for pageId in self.pageIds():
            fields += self.page(pageId).fields
        return fields

    def getFieldsMap(self):
        fieldsDir = {}
        for name in self.getFieldsNames():
            fieldsDir[name] = self.field(name)
        return fieldsDir

    def _onNextCLicked(self):
        currentPage = self.page(self.currentId() - 1)
        currentPage.onNextClicked()

    def _onFinishedClicked(self):
        try:
            print(self.getFieldsMap())
        except Exception as e:
            print(e)
        self.restart()
