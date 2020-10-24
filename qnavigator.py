# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 23:01:01 2020

@author: Marcin
"""

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWizard
from qnavigatorpages import *


class Navigator(QWizard):
    def __init__(self):
        super(Navigator, self).__init__()
        self.setWindowTitle("Add patient record")
        self.setWizardStyle(QWizard.ModernStyle)
        self.setWindowIcon(QtGui.QIcon('tooth.png'))
        # TODO: find out why only Watermark works here! Banner and Logo not working
        # self.setPixmap(QWizard.WatermarkPixmap, QPixmap('steth.png'))
        # TODO: add all necessary pages
        self.addPage(PersonalDataPage())
