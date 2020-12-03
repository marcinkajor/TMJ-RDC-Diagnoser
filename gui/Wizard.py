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
        super(Wizard, self).__init__()
        self.database = database
        self.button(QWizard.NextButton).clicked.connect(self._onNextCLicked)
        self.button(QWizard.FinishButton).clicked.connect(self.restart)
        self.setWindowTitle("Add patient record")
        self.setWizardStyle(QWizard.ModernStyle)
        self.setWindowIcon(QIcon('../tooth.png'))
        # TODO: find out why only Watermark works here! Banner and Logo not working
        # self.setPixmap(QWizard.WatermarkPixmap, QPixmap('steth.png'))
        # TODO: add all necessary pages
        self.addPage(PersonalDataPage(self.database))
        self.addPage(InitialDataPage(self.database))
        self.addPage(AbductionMovementPage(self.database))
        self.addPage(VerticalMovementRangePage(self.database))
        self.addPage(IncisorsGapPage(self.database))
        self.addPage(VerticalMandibleMovementsPage(self.database))
        self.addPage(SoundsInJointAbductionPage(self.database))
        self.addPage(SoundsInJointHorizontalMovementsPage(self.database))

    def _onNextCLicked(self):
        currentPage = self.page(self.currentId() - 1)
        currentPage.onNextClicked()
