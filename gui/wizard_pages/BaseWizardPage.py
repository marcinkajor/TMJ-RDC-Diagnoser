from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QWizardPage


class BasePage(QWizardPage):
    defaultFont = QFont("Arial", 10)

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('../../tooth.png'))
        self.fields = []

    def onNextClicked(self):
        pass

    def registerField(self, name, widget, property=None, changedSignal=None):
        nameSplit = name.split()
        extendedName = self.getClassName() + '/' + "_".join(nameSplit)
        super().registerField(extendedName, widget, property=property, changedSignal=changedSignal)
        self.fields.append(extendedName)

    def getClassName(self):
        return self.__class__.__name__.split('.')[-1]
