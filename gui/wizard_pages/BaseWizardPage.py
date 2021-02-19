from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QWizardPage
from gui.wizard_pages.WizardPagesHelpers import SideOptions


class BasePage(QWizardPage):
    defaultFont = QFont("Arial", 10)

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('../../tooth.png'))
        self.fields = []

    def onNextClicked(self):
        pass

    def registerField(self, name, widget, property=None, changedSignal=None, mandatory=False):
        if mandatory:
            name += '*'
        extendedName = self._cleanFieldName(name)
        super().registerField(extendedName, widget, property=property, changedSignal=changedSignal)
        noAsteriskName = extendedName.replace('*', "")
        self.fields.append(noAsteriskName)

    def _cleanFieldName(self, name):
        cleanName = name.replace('"', "")
        cleanName = cleanName.replace('-', "")
        cleanName = cleanName.replace('(', "")
        cleanName = cleanName.replace(')', "")
        cleanName = cleanName.replace(',', "")
        cleanName = cleanName.replace(':', "")
        cleanName = cleanName.replace('/', "_")
        cleanName = cleanName.lower()
        nameSplit = cleanName.split()
        return self.getClassName() + '/' + "_".join(nameSplit)

    def getClassName(self):
        return self.__class__.__name__.split('.')[-1]

    def clearAll(self):
        pass

    def loadWithData(self, patientID):
        self.doLoadWithData(patientID)
        self.completeChanged.emit()

    def doLoadWithData(self, patientID):
        pass


class PageWithSideOptions(BasePage):
    def __init__(self):
        self.painOptions = SideOptions([], [], None)  # filled in each subclass
        super().__init__()

    def registerSideOptions(self, isMandatory=False):
        if self.painOptions:
            rightOptions = self.painOptions.getRightOptions().getOptions()
            for rightOptionName in rightOptions:
                rightButtonGroup = rightOptions[rightOptionName]
                self.registerField(rightOptionName + ' right', rightButtonGroup, property="checkedButton",
                                   changedSignal=rightButtonGroup.buttonClicked, mandatory=isMandatory)
            leftOptions = self.painOptions.getLeftOptions().getOptions()
            for leftOptionName in leftOptions:
                leftButtonGroup = leftOptions[leftOptionName]
                self.registerField(leftOptionName + ' left', leftButtonGroup, property="checkedButton",
                                   changedSignal=leftButtonGroup.buttonClicked, mandatory=isMandatory)
