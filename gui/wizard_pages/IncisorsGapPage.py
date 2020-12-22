from gui.wizard_pages.BaseWizardPage import BasePage
from gui.wizard_pages.WizardPagesHelpers import *


class IncisorsGapPage(BasePage):
    def __init__(self):
        super().__init__()
        self.setTitle("4. Incisors gap")

        self.mm = MmInputs(["Vertical", "Horizontal", "Middle line"], "mm", self.defaultFont)
        mmLineEdits = self.mm.getAllLineEdits()
        for lineEditName in mmLineEdits:
            self.registerField(mmLineEdits[lineEditName].objectName(), mmLineEdits[lineEditName], mandatory=True)

        self.middleLineAlignment = ButtonGroupBox("Middle line alignment relative to the jaw", ["R", "L"],
                                                  layout='horizontal')
        self.registerField(self.middleLineAlignment.getName(), self.middleLineAlignment, property="checkedButton",
                           changedSignal=self.middleLineAlignment.buttonClicked, mandatory=True)
        self.middleLineAlignment.getWidget().setFont(self.defaultFont)

        rightLayout = QHBoxLayout()
        rightLayout.addWidget(self.middleLineAlignment.getWidget())
        mainLayout = QGridLayout()

        mainLayout.addWidget(self.mm.getWidget(), 0, 0)
        mainLayout.addLayout(rightLayout, 0, 1)
        self.setLayout(mainLayout)

    def clearAll(self):
        self.middleLineAlignment.clearAll()
