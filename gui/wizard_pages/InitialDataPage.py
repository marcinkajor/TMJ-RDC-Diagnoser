from gui.wizard_pages.BaseWizardPage import BasePage
from gui.wizard_pages.WizardPagesHelpers import *
from algo.DatabaseDeserializer import DatabaseDeserializer


class InitialDataPage(BasePage):
    def __init__(self):
        super().__init__()

        self.NO_PAIN = "None"
        self.RIGHT = "Right"
        self.LEFT = "Left"
        self.BOTH = "Both"

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

    def _customIsComplete(self):
        if self.painSideBox.isChecked():
            currentOption = self.painSideBox.checkedButton
            if currentOption == self.NO_PAIN:
                return True
            elif currentOption == self.RIGHT:
                return True if self.rightOptionsGroup.isChecked() else False
            elif currentOption == self.LEFT:
                return True if self.leftOptionsGroup.isChecked() else False
            elif currentOption == self.BOTH:
                return True if self.rightOptionsGroup.isChecked() and self.leftOptionsGroup.isChecked() else False
            else:
                return False
        else:
            return False

    def isComplete(self):
        try:
            return self._customIsComplete()
        except Exception as e:
            print(e)

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
        self.completeChanged.emit()

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
        options = ["Muscles", "Jaw Joint", "Both"]
        self.optionsGridLayout = QHBoxLayout()

        self.rightOptionsGroup = ButtonGroupBox("Right", options, layout='horizontal')
        self.rightOptionsGroup.registerClickCallback(self.completeChanged.emit)
        self.registerField("Right pain area", self.rightOptionsGroup,
                           property="checkedButton",
                           changedSignal=self.rightOptionsGroup.buttonClicked)

        self.leftOptionsGroup = ButtonGroupBox("Left", options, layout='horizontal')
        self.leftOptionsGroup.registerClickCallback(self.completeChanged.emit)
        self.registerField("Left pain area", self.leftOptionsGroup,
                           property="checkedButton",
                           changedSignal=self.leftOptionsGroup.buttonClicked)

        self.optionsGridLayout.addWidget(self.rightOptionsGroup.getWidget())
        self.optionsGridLayout.addWidget(self.leftOptionsGroup.getWidget())
        self._enablePainOptions(right=False, left=False)
        self.painAreaBox = QGroupBox("Pain area")
        self.painAreaBox.setLayout(self.optionsGridLayout)
        return self.painAreaBox

    def clearAll(self):
        self.painSideBox.clearAll()
        self._enablePainOptions(False, False)

    def doLoadWithData(self, patientId):
        serializer = DatabaseDeserializer(self.wizard().getDatabase())
        diagnosticData = serializer.getDiagnosticDataDictById(patientId)
        initialData = diagnosticData["InitialData"]
        painSide = initialData["pain_side"]
        rightPainArea = initialData["right_pain_area"]
        leftPainArea = initialData["left_pain_area"]

        self.painSideBox.getButton(painSide).setChecked(True)
        if rightPainArea:
            self.rightOptionsGroup.getButton(rightPainArea).setChecked(True)
        if leftPainArea:
            self.leftOptionsGroup.getButton(leftPainArea).setChecked(True)
        self._onButtonGroupChanged()
