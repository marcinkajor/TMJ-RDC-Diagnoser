# -*- coding: utf-8 -*-
"""
Created on Tue May  5 19:49:43 2020

@author: Marcin
"""

from PyQt5 import QtWidgets, QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QAction, QFileDialog
import sys
import pandas as pd

class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
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
        openAction.triggered.connect(QtWidgets.QApplication.quit)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        fileMenu.addAction(quitAction)
        fileMenu.addAction(openAction)

        self.show()

    # handle close button of the main window (quit QApplication properly)
    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Window close", "Close the Diagnoser?",
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if (reply == QMessageBox.Yes):
            event.accept()
            QtWidgets.QApplication.quit()
        else:
            event.ignore()

    def openFile(self):
        fileName, fileFilter = QFileDialog.getOpenFileName(self, 'Open File',
                                               filter="Excel files (*.xlsx)")

        print(fileName)
        axis1_sheet = pd.read_excel(fileName, sheet_name = 'axis I')
        palpation_sheet = pd.read_excel(fileName, sheet_name = 'axis I palpacja')
        q_sheet = pd.read_excel(fileName, sheet_name = 'Q')

if __name__ == "__main__":
    def run():
        app = QtWidgets.QApplication(sys.argv)
        window = Window()
        app.exec_()
    run()
