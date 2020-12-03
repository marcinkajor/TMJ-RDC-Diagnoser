from gui.wizard_pages.BaseWizardPage import BasePage
from gui.wizard_pages.WiardPagesHelpers import *


class VerticalMovementRangePage(BasePage):
    def __init__(self, database):
        super(BasePage, self).__init__()
        self.setTitle("3. Vertical movement range")
        self.database = database

        self.usedForetooth = ButtonGroupBox("Used foretooth", ["11", "21"], layout='horizontal')
        self.usedForetooth.getWidget().setFont(self.defaultFont)

        self.mm = MmInputs(["No pain opening", "Max active opening", "Max passive opening"], self.defaultFont)

        rightLayout = QHBoxLayout()
        self.painOptions = PainOptions(["Max active opening", "Max passive opening"], self.defaultFont)
        rightLayout.addLayout(self.painOptions.getLayout())
        mainLayout = QGridLayout()

        mainLayout.addWidget(self.usedForetooth.getWidget(), 0, 0)
        mainLayout.addWidget(self.mm.getWidget(), 1, 0)
        mainLayout.addLayout(rightLayout, 1, 1)
        self.setLayout(mainLayout)

