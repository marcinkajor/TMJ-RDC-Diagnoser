# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 23:01:01 2020

@author: Marcin
"""

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QWizard, QLineEdit, QWizardPage
from qnavigatorpages import *


class Navigator(QWizard):
    def __init__(self):
        super(Navigator, self).__init__()
        self.setWindowTitle("Add patient record")
        self.setWizardStyle(QWizard.ModernStyle)
        self.setWindowIcon(QtGui.QIcon('tooth.png'))

        # TODO: add all necessary pages
        self.addPage(PersonalDataPage())
