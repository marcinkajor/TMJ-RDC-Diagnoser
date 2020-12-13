from gui.wizard_pages.BaseWizardPage import BasePage
from gui.wizard_pages.WizardPagesHelpers import *


class SoundsInJointHorizontalMovementsPage(BasePage):
    def __init__(self, database):
        super().__init__()
        self.setTitle("6. Sounds in the joint: horizontal movements")
        self.database = database

        self.painOptions = SideOptions(["Right side", "Left side", "Forward"],
                                       ["None", "Click", "Clear crepitations", "Slight crepitations"], self.defaultFont)

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

        additionalInfo = QLabel("(>=2 x 3 attempts, during movement)")
        additionalInfo.setFont(self.defaultFont)
        rightLayout = QHBoxLayout()
        rightLayout.addLayout(self.painOptions.getLayout())
        mainLayout = QGridLayout()
        mainLayout.addWidget(additionalInfo, 0, 0)
        mainLayout.addLayout(rightLayout, 1, 0)
        self.setLayout(mainLayout)
