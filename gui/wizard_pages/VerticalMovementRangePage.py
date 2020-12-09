from gui.wizard_pages.BaseWizardPage import BasePage
from gui.wizard_pages.WizardPagesHelpers import *

'''
Fields:
    - "VerticalMovementRangePage/Used_foretooth"
    - "VerticalMovementRangePage/No_pain_opening_mm"
    - "VerticalMovementRangePage/Max_active_opening_mm"
    - "VerticalMovementRangePage/Max_passive_opening_mm"
    - "VerticalMovementRangePage/Max_active_opening_right"
    - "VerticalMovementRangePage/Max_passive_opening_right"
    - "VerticalMovementRangePage/Max_active_opening_mm"
    - "VerticalMovementRangePage/Max_active_opening_left"
'''


class VerticalMovementRangePage(BasePage):
    def __init__(self, database):
        super().__init__()
        self.setTitle("3. Vertical movement range")
        self.database = database

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

        rightLayout.addLayout(self.painOptions.getLayout())
        mainLayout = QGridLayout()

        mainLayout.addWidget(self.usedForetooth.getWidget(), 0, 0)
        mainLayout.addWidget(self.mm.getWidget(), 1, 0)
        mainLayout.addLayout(rightLayout, 1, 1)
        self.setLayout(mainLayout)

