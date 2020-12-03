from gui.wizard_pages.BaseWizardPage import BasePage
from gui.wizard_pages.WiardPagesHelpers import *


class IncisorsGapPage(BasePage):
    def __init__(self, database):
        super(BasePage, self).__init__()
        self.setTitle("4. Incisors gap")
        self.database = database

        self.mm = MmInputs(["Vertical", "Horizontal", "Middle line"], "mm", self.defaultFont)

        self.middleLineAlignment = ButtonGroupBox("Middle line alignment relative to the jaw", ["R", "L"],
                                                  layout='horizontal')
        self.middleLineAlignment.getWidget().setFont(self.defaultFont)

        rightLayout = QHBoxLayout()
        rightLayout.addWidget(self.middleLineAlignment.getWidget())
        mainLayout = QGridLayout()

        mainLayout.addWidget(self.mm.getWidget(), 0, 0)
        mainLayout.addLayout(rightLayout, 0, 1)
        self.setLayout(mainLayout)
