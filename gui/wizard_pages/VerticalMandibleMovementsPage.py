from gui.wizard_pages.BaseWizardPage import BasePage
from gui.wizard_pages.WiardPagesHelpers import *


class VerticalMandibleMovementsPage(BasePage):
    def __init__(self, database):
        super(BasePage, self).__init__()
        self.setTitle("5. Vertical mandible movements")
        self.database = database

        self.mm = MmInputs(["Right side", "Left side", "Forward"], "mm", self.defaultFont)
        self.painOptions = SideOptions(["Right side", "Left side", "Forward"], ["None", "Muscle", "Join", "Both"],
                                       self.defaultFont)

        rightLayout = QHBoxLayout()
        rightLayout.addLayout(self.painOptions.getLayout())
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.mm.getWidget(), 0, 0)
        mainLayout.addLayout(rightLayout, 0, 1)
        self.setLayout(mainLayout)

