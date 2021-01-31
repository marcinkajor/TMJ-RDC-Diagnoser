from gui.wizard_pages.BaseWizardPage import PageWithSideOptions
from gui.wizard_pages.WizardPagesHelpers import *


class SoundsInJointHorizontalMovementsPage(PageWithSideOptions):
    def __init__(self):
        super().__init__()
        self.setTitle("6. Sounds in the joint: horizontal movements")

        self.painOptions = SideOptions(["Right side", "Left side", "Forward"],
                                       ["None", "Click", "Clear crepitations", "Slight crepitations"], self.defaultFont)
        self.registerSideOptions(isMandatory=True)

        additionalInfo = QLabel("(>=2 x 3 attempts, during movement)")
        additionalInfo.setFont(self.defaultFont)
        rightLayout = QHBoxLayout()
        rightLayout.addLayout(self.painOptions.getLayout())
        mainLayout = QGridLayout()
        mainLayout.addWidget(additionalInfo, 0, 0)
        mainLayout.addLayout(rightLayout, 1, 0)
        self.setLayout(mainLayout)

    def clearAll(self):
        self.painOptions.clearAll()
