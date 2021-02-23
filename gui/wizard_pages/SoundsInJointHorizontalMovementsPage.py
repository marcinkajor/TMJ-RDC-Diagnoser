from gui.wizard_pages.BaseWizardPage import PageWithSideOptions
from gui.wizard_pages.WizardPagesHelpers import *
from algo.DatabaseDeserializer import DatabaseDeserializer


class SoundsInJointHorizontalMovementsPage(PageWithSideOptions):
    def __init__(self):
        super().__init__()
        self.setTitle("6. Sounds in the joint: horizontal movements")

        self.painOptions = SideOptions(["Right side", "Left side", "Forward"],
                                       ["None", "Click", "Coarse Crepitus", "Fine Crepitus"], self.defaultFont)
        self.registerSideOptions(isMandatory=True)

        additionalInfo = QLabel("(>=2 x 3 attempts, during movement)")
        additionalInfo.setFont(self.defaultFont)
        rightLayout = QHBoxLayout()
        rightLayout.addLayout(self.painOptions.getLayout())
        mainLayout = QGridLayout()
        mainLayout.addWidget(additionalInfo, 0, 0)
        mainLayout.addLayout(rightLayout, 1, 0)
        self.setLayout(mainLayout)

    def clearAll(self):
        self.painOptions.clearAll()

    def doLoadWithData(self, patientId):
        serializer = DatabaseDeserializer(self.wizard().getDatabase())
        diagnosticData = serializer.getDiagnosticDataDictById(patientId)
        soundsInJointHorizontalMovementsData = diagnosticData["SoundsInJointHorizontalMovements"]

        rightRightSide = soundsInJointHorizontalMovementsData["right_side_right"]
        leftRightSide = soundsInJointHorizontalMovementsData["left_side_right"]
        forwardRight = soundsInJointHorizontalMovementsData["forward_right"]
        rightSideLeft = soundsInJointHorizontalMovementsData["right_side_left"]
        leftSideLeft = soundsInJointHorizontalMovementsData["left_side_left"]
        forwardLeft = soundsInJointHorizontalMovementsData["forward_left"]

        soundOptions = self.painOptions.getRightOptions().getOptions()
        soundOptions["Right side"].getButton(rightRightSide).setChecked(True)
        soundOptions["Left side"].getButton(leftRightSide).setChecked(True)
        soundOptions["Forward"].getButton(forwardRight).setChecked(True)

        soundOptions = self.painOptions.getLeftOptions().getOptions()
        soundOptions["Right side"].getButton(rightSideLeft).setChecked(True)
        soundOptions["Left side"].getButton(leftSideLeft).setChecked(True)
        soundOptions["Forward"].getButton(forwardLeft).setChecked(True)
