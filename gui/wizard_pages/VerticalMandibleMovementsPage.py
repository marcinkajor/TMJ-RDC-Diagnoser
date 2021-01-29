from gui.wizard_pages.BaseWizardPage import PageWithSideOptions
from gui.wizard_pages.WizardPagesHelpers import *


class VerticalMandibleMovementsPage(PageWithSideOptions):
    def __init__(self):
        super().__init__()
        self.setTitle("5. Vertical mandible movements")

        self.mm = MmInputs(["Right side", "Left side", "Forward"], "mm", self.defaultFont)
        mmLineEdits = self.mm.getAllLineEdits()
        for lineEditName in mmLineEdits:
            self.registerField(mmLineEdits[lineEditName].objectName(), mmLineEdits[lineEditName])

        self.painOptions = SideOptions(["Right side", "Left side", "Forward"], ["None", "Muscle", "Joint", "Both"],
                                       self.defaultFont)
        self.registerSideOptions()

        rightLayout = QHBoxLayout()
        rightLayout.addLayout(self.painOptions.getLayout())
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.mm.getWidget(), 0, 0)
        mainLayout.addLayout(rightLayout, 0, 1)
        self.setLayout(mainLayout)

    def clearAll(self):
        self.painOptions.clearAll()

