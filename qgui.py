# -*- coding: utf-8 -*-
"""
Created on Tue May  5 19:49:43 2020

@author: Marcin
"""

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
import sys
import pandas as pd

class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("TMJ RDC Diagnoser")
        self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))

        quitAction = QAction("Open", self)
        quitAction.setShortcut("Ctrl+O")
        quitAction.setStatusTip('Open the examination file')
        quitAction.triggered.connect(self.openFile)

        openAction = QAction("Quit", self)
        openAction.setShortcut("Ctrl+Q")
        openAction.setStatusTip('Quit the application')
        openAction.triggered.connect(self.closeApp)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        fileMenu.addAction(quitAction)
        fileMenu.addAction(openAction)

        self.quitButton()

    def quitButton(self):
        btn = QPushButton("Quit", self)
        btn.clicked.connect(self.closeApp)
        btn.resize(btn.minimumSizeHint())
        btn.move(200,150)
        self.show()

    def openFile(self):
        fileName, fileFilter = QFileDialog.getOpenFileName(self, 'Open File',
                                               filter="Excel files (*.xlsx)")

        print(fileName)
        axis1_sheet = pd.read_excel(fileName, sheet_name = 'axis I')
        palpation_sheet = pd.read_excel(fileName, sheet_name = 'axis I palpacja')
        q_sheet = pd.read_excel(fileName, sheet_name = 'Q')

    def closeApp(self):
        sys.exit()


def run():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
