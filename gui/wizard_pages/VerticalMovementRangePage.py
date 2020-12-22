from gui.wizard_pages.BaseWizardPage import PageWithSideOptions
from gui.wizard_pages.WizardPagesHelpers import *


class VerticalMovementRangePage(PageWithSideOptions):
    def __init__(self):
        super().__init__()
        self.setTitle("3. Vertical movement range")

        self.usedForetooth = ButtonGroupBox("Used foretooth", ["11", "21"], layout='horizontal')
        self.registerField("Used foretooth", self.usedForetooth,
                           property="checkedButton",
                           changedSignal=self.usedForetooth.buttonClicked)
        self.usedForetooth.getWidget().setFont(self.defaultFont)

        self.mm = MmInputs(["No pain opening", "Max active opening", "Max passive opening"], "mm", self.defaultFont)

        mmLineEdits = self.mm.getAllLineEdits()
        for lineEditName in mmLineEdits:
            self.registerField(mmLineEdits[lineEditName].objectName(), mmLineEdits[lineEditName])

        rightLayout = QHBoxLayout()
        self.painOptions = SideOptions(["Max active opening", "Max passive opening"],
                                       ["None", "Muscle", "Join", "Both"], self.defaultFont)
        self.registerSideOptions()

        rightLayout.addLayout(self.painOptions.getLayout())
        mainLayout = QGridLayout()

        mainLayout.addWidget(self.usedForetooth.getWidget(), 0, 0)
        mainLayout.addWidget(self.mm.getWidget(), 1, 0)
        mainLayout.addLayout(rightLayout, 1, 1)
        self.setLayout(mainLayout)

    def clearAll(self):
        self.painOptions.clearAll()
        self.usedForetooth.clearAll()