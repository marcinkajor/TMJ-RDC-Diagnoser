from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QWizardPage


class BasePage(QWizardPage):
    defaultFont = QFont("Arial", 10)

    def __init__(self):
        super(QWizardPage, self).__init__()
        self.setWindowIcon(QIcon('../../tooth.png'))

    def onNextClicked(self):
        pass
