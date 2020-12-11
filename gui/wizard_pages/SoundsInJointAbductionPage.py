from gui.wizard_pages.BaseWizardPage import BasePage
from gui.wizard_pages.WizardPagesHelpers import *


class SoundsInJointAbductionPage(BasePage):
    def __init__(self, database):
        super().__init__()
        self.setTitle("6. Sounds in the joint: abduction")
        self.database = database

        self.mm = MmInputs(["Left: opening", "Left: closing", "Right: opening", "Right: closing"],
                           "Click position - mm",
                           self.defaultFont)

        mmLineEdits = self.mm.getAllLineEdits()
        for lineEditName in mmLineEdits:
            self.registerField(mmLineEdits[lineEditName].objectName(), mmLineEdits[lineEditName])

        self.clickEliminationOptions = Options("Click elimination", ["Left opening", "Left closing", "Right opening",
                                                                     "Right closing"],
                                               ["No", "Yes", "Not applicable"], self.defaultFont)

        rawClickEliminationOptions = self.clickEliminationOptions.getOptions()
        for option in rawClickEliminationOptions:
            buttonGroup = rawClickEliminationOptions[option]
            self.registerField(option + ' click elimination', buttonGroup, property="checkedButton",
                               changedSignal=buttonGroup.buttonClicked)

        self.soundsOptions = Options("Sounds", ["Left opening", "Left closing", "Right opening", "Right closing"],
                                     ["None", "Click", "Clear crepitations", "Slight crepitations"], self.defaultFont)

        rawSoundsOptions = self.clickEliminationOptions.getOptions()
        for option in rawSoundsOptions:
            buttonGroup = rawSoundsOptions[option]
            self.registerField(option + ' sound', buttonGroup, property="checkedButton",
                               changedSignal=buttonGroup.buttonClicked)

        additionalInfo = QLabel("(2 ouf of 3 attempts, palpation during abduction)")
        additionalInfo.setFont(self.defaultFont)

        mainLayout = QGridLayout()

        mainLayout.addWidget(additionalInfo, 0, 0)
        mainLayout.addLayout(self.soundsOptions.getLayout(), 1, 0)
        mainLayout.addWidget(self.mm.getWidget(), 1, 1)
        mainLayout.addLayout(self.clickEliminationOptions.getLayout(), 1, 2)

        self.setLayout(mainLayout)

    # TODO: remove, it's only for fields testing
    def onNextClicked(self):
        try:
            print(self.wizard().getFieldsMap())
        except Exception as e:
            print(e)

