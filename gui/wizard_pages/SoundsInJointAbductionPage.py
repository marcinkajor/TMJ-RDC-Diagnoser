from gui.wizard_pages.BaseWizardPage import BasePage
from gui.wizard_pages.WizardPagesHelpers import *
from algo.DatabaseDeserializer import DatabaseDeserializer


class SoundsInJointAbductionPage(BasePage):
    def __init__(self):
        super().__init__()
        self.setTitle("6. Sounds in the joint: abduction")

        self.mm = MmInputs(["Left: opening", "Left: closing", "Right: opening", "Right: closing"],
                           "Measurement of Click - mm",
                           self.defaultFont)

        mmLineEdits = self.mm.getAllLineEdits()
        for lineEditName in mmLineEdits:
            self.registerField(mmLineEdits[lineEditName].objectName(), mmLineEdits[lineEditName])

        self.clickEliminationOptions = Options("Reciprocal click eliminated on protrusive opening",
                                               ["Left opening", "Left closing", "Right opening", "Right closing"],
                                               ["No", "Yes", "Not Applicable"], self.defaultFont)

        rawClickEliminationOptions = self.clickEliminationOptions.getOptions()
        for option in rawClickEliminationOptions:
            buttonGroup = rawClickEliminationOptions[option]
            self.registerField(option + ' click elimination', buttonGroup, property="checkedButton",
                               changedSignal=buttonGroup.buttonClicked, mandatory=True)

        self.soundsOptions = Options("Sounds", ["Left opening", "Left closing", "Right opening", "Right closing"],
                                     ["None", "Click", "Coarse Crepitus", "Fine Crepitus"], self.defaultFont)

        rawSoundsOptions = self.soundsOptions.getOptions()
        for option in rawSoundsOptions:
            buttonGroup = rawSoundsOptions[option]
            self.registerField(option + ' sound', buttonGroup, property="checkedButton",
                               changedSignal=buttonGroup.buttonClicked, mandatory=True)

        additionalInfo = QLabel("(2 ouf of 3 attempts, palpation during abduction)")
        additionalInfo.setFont(self.defaultFont)

        mainLayout = QGridLayout()

        mainLayout.addWidget(additionalInfo, 0, 0)
        mainLayout.addLayout(self.soundsOptions.getLayout(), 1, 0)
        mainLayout.addWidget(self.mm.getWidget(), 1, 1)
        mainLayout.addLayout(self.clickEliminationOptions.getLayout(), 1, 2)

        self.setLayout(mainLayout)

    def clearAll(self):
        self.clickEliminationOptions.cleaAll()
        self.soundsOptions.cleaAll()

    def doLoadWithData(self, patientId):
        serializer = DatabaseDeserializer(self.wizard().getDatabase())
        diagnosticData = serializer.getDiagnosticDataDictById(patientId)
        soundsInJointAbductionData = diagnosticData["SoundsInJointAbduction"]

        leftOpeningMm = soundsInJointAbductionData["left_opening_mm"]
        leftClosingMm = soundsInJointAbductionData["left_closing_mm"]

        rightOpeningMm = soundsInJointAbductionData["right_opening_mm"]
        rightClosingMm = soundsInJointAbductionData["right_closing_mm"]

        leftOpeningClickElimination = soundsInJointAbductionData["left_opening_click_elimination"]
        leftClosingClickElimination = soundsInJointAbductionData["left_closing_click_elimination"]

        rightOpeningClickElimination = soundsInJointAbductionData["right_opening_click_elimination"]
        rightClosingClickElimination = soundsInJointAbductionData["right_closing_click_elimination"]

        leftOpeningSound = soundsInJointAbductionData["left_opening_sound"]
        leftClosingSound = soundsInJointAbductionData["left_closing_sound"]

        rightOpeningSound = soundsInJointAbductionData["right_opening_sound"]
        rightClosingSound = soundsInJointAbductionData["right_closing_sound"]

        self.mm.getLineEdit("Left: opening").setText(leftOpeningMm)
        self.mm.getLineEdit("Left: closing").setText(leftClosingMm)
        self.mm.getLineEdit("Right: opening").setText(rightOpeningMm)
        self.mm.getLineEdit("Right: closing").setText(rightClosingMm)

        clickOptions = self.clickEliminationOptions.getOptions()
        clickOptions["Left opening"].getButton(leftOpeningClickElimination).setChecked(True)
        clickOptions["Left closing"].getButton(leftClosingClickElimination).setChecked(True)
        clickOptions["Right opening"].getButton(rightOpeningClickElimination).setChecked(True)
        clickOptions["Right closing"].getButton(rightClosingClickElimination).setChecked(True)

        soundOptions = self.soundsOptions.getOptions()
        soundOptions["Left opening"].getButton(leftOpeningSound).setChecked(True)
        soundOptions["Left closing"].getButton(leftClosingSound).setChecked(True)
        soundOptions["Right opening"].getButton(rightOpeningSound).setChecked(True)
        soundOptions["Right closing"].getButton(rightClosingSound).setChecked(True)
