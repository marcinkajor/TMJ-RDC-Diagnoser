from gui.wizard_pages.BaseWizardPage import BasePage
from gui.wizard_pages.WizardPagesHelpers import *


class VerticalMandibleMovementsPage(BasePage):
    def __init__(self, database):
        super().__init__()
        self.setTitle("5. Vertical mandible movements")
        self.database = database

        self.mm = MmInputs(["Right side", "Left side", "Forward"], "mm", self.defaultFont)
        mmLineEdits = self.mm.getAllLineEdits()
        for lineEditName in mmLineEdits:
            self.registerField(mmLineEdits[lineEditName].objectName(), mmLineEdits[lineEditName])

        self.painOptions = SideOptions(["Right side", "Left side", "Forward"], ["None", "Muscle", "Join", "Both"],
                                       self.defaultFont)

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

        rightLayout = QHBoxLayout()
        rightLayout.addLayout(self.painOptions.getLayout())
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.mm.getWidget(), 0, 0)
        mainLayout.addLayout(rightLayout, 0, 1)
        self.setLayout(mainLayout)

