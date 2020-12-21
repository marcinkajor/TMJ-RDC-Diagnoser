from gui.wizard_pages.BaseWizardPage import BasePage
from gui.wizard_pages.WizardPagesHelpers import *

'''
Fields:
    - "InitialDataPage/Pain_side"
    - "InitialDataPage/Right_pain_area"
    - "InitialDataPage/Left_pain_area"
'''


class InitialDataPage(BasePage):
    def __init__(self):
        super().__init__()

        self.NO_PAIN = "NO PAIN"
        self.RIGHT = "RIGHT"
        self.LEFT = "LEFT"
        self.BOTH = "BOTH"

        self.mapping = {
            self.NO_PAIN: 0,
            self.RIGHT: 1,
            self.LEFT: 2,
            self.BOTH: 3
        }

        self.setTitle("1. Initial patient interview")
        self.grid = QGridLayout()
        self.painSideBox = ButtonGroupBox("Pain side", [self.NO_PAIN, self.RIGHT, self.LEFT, self.BOTH],
                                          layout='horizontal')
        self.painSideBox.registerClickCallback(self._onButtonGroupChanged)
        self.registerField("Pain side", self.painSideBox,
                           property="checkedButton",
                           changedSignal=self.painSideBox.buttonClicked)
        self.painAreaBox = self._generatePainOptions()
        self.majorBox = QGroupBox("Facial pain")
        self.majorBox.setFont(self.defaultFont)
        vLayout = QVBoxLayout()
        vLayout.addWidget(self.painSideBox.getWidget())
        vLayout.addWidget(self.painAreaBox)
        self.majorBox.setLayout(vLayout)
        self.grid.addWidget(self.majorBox)
        self.setLayout(self.grid)

    def _onButtonGroupChanged(self):
        currentOption = self.painSideBox.checkedButton
        if currentOption is None:
            return
        if currentOption != self.NO_PAIN:
            self.painSideBox.setEnabled(True)
            if currentOption == self.RIGHT:
                self._enablePainOptions(right=True, left=False)
            elif currentOption == self.LEFT:
                self._enablePainOptions(right=False, left=True)
            else:
                self._enablePainOptions(right=True, left=True)
        else:
            self._enablePainOptions(left=False, right=False)

    def _enablePainOptions(self, right, left):
        if right and not left:
            self.leftOptionsGroup.clearAll()
        if left and not right:
            self.rightOptionsGroup.clearAll()
        if not left and not right:
            self.rightOptionsGroup.clearAll()
            self.leftOptionsGroup.clearAll()
        self.rightOptionsGroup.enableAll(right)
        self.leftOptionsGroup.enableAll(left)

    def _generatePainOptions(self):
        options = ["Muscle", "Join", "Both"]
        self.optionsGridLayout = QHBoxLayout()

        self.rightOptionsGroup = ButtonGroupBox("Right", options, layout='horizontal')
        self.registerField("Right pain area", self.rightOptionsGroup,
                           property="checkedButton",
                           changedSignal=self.rightOptionsGroup.buttonClicked)

        self.leftOptionsGroup = ButtonGroupBox("Left", options, layout='horizontal')
        self.registerField("Left pain area", self.leftOptionsGroup,
                           property="checkedButton",
                           changedSignal=self.leftOptionsGroup.buttonClicked)

        self.optionsGridLayout.addWidget(self.rightOptionsGroup.getWidget())
        self.optionsGridLayout.addWidget(self.leftOptionsGroup.getWidget())
        self._enablePainOptions(right=False, left=False)
        self.painAreaBox = QGroupBox("Pain area")
        self.painAreaBox.setLayout(self.optionsGridLayout)
        return self.painAreaBox
