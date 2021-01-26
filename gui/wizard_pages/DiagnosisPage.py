from gui.wizard_pages.BaseWizardPage import BasePage
from PyQt5.QtWidgets import QGroupBox, QRadioButton, QVBoxLayout, QButtonGroup, QWidget, QHBoxLayout, \
    QLabel, QLineEdit, QGridLayout, QPushButton
from algo.DatabaseMapper import DatabaseRecordMapper


class DiagnosisPage(BasePage):
    def __init__(self):
        super().__init__()
        self.setTitle("RDC Diagnosis")
        self.button = QPushButton("Get diagnosis")
        self.label = QLabel("")
        self.button.clicked.connect(self.printDiagnosis)

    def printDiagnosis(self):
        pass

    def onNextClicked(self):
        pass

