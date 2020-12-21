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

    def registerField(self, name, widget, property=None, changedSignal=None):
        cleanName = name.replace('"', "")
        cleanName = cleanName.replace('-', "")
        cleanName = cleanName.replace('(', "")
        cleanName = cleanName.replace(')', "")
        cleanName = cleanName.replace(',', "")
        cleanName = cleanName.replace(':', "")
        cleanName = cleanName.replace('/', "_")
        cleanName = cleanName.lower()
        nameSplit = cleanName.split()
        extendedName = self.getClassName() + '/' + "_".join(nameSplit)
        super().registerField(extendedName, widget, property=property, changedSignal=changedSignal)
        self.fields.append(extendedName)

    def getClassName(self):
        return self.__class__.__name__.split('.')[-1]

    def clearAll(self):
        pass


class PageWithSideOptions(BasePage):
    def __init__(self):
        self.painOptions = SideOptions([], [], None)  # filled in each subclass
        super().__init__()

    def registerSideOptions(self):
        if self.painOptions:
            rightOptions = self.painOptions.getRightOptions().getOptions()
            for rightOptionName in rightOptions:
                rightButtonGroup = rightOptions[rightOptionName]
                self.registerField(rightOptionName + ' right', rightButtonGroup, property="checkedButton",
                                   changedSignal=rightButtonGroup.buttonClicked)
            leftOptions = self.painOptions.getLeftOptions().getOptions()
            for leftOptionName in leftOptions:
                leftButtonGroup = leftOptions[leftOptionName]
                self.registerField(leftOptionName + ' left', leftButtonGroup, property="checkedButton",
                                   changedSignal=leftButtonGroup.buttonClicked)
