from gui.wizard_pages.BaseWizardPage import PageWithSideOptions
from gui.wizard_pages.WizardPagesHelpers import *
from algo.DatabaseDeserializer import DatabaseDeserializer


class VerticalMandibleMovementsPage(PageWithSideOptions):
    def __init__(self):
        super().__init__()
        self.setTitle("5. Vertical mandible movements")

        self.mm = MmInputs(["Right side", "Left side", "Forward"], "mm", self.defaultFont)
        mmLineEdits = self.mm.getAllLineEdits()
        for lineEditName in mmLineEdits:
            self.registerField(mmLineEdits[lineEditName].objectName(), mmLineEdits[lineEditName], mandatory=True)

        self.painOptions = SideOptions(["Right side", "Left side", "Forward"], ["None", "Muscle", "Joint", "Both"],
                                       self.defaultFont)
        self.registerSideOptions(isMandatory=True)

        rightLayout = QHBoxLayout()
        rightLayout.addLayout(self.painOptions.getLayout())
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.mm.getWidget(), 0, 0)
        mainLayout.addLayout(rightLayout, 0, 1)
        self.setLayout(mainLayout)

    def clearAll(self):
        self.painOptions.clearAll()

    def doLoadWithData(self, patientId):
        serializer = DatabaseDeserializer(self.wizard().getDatabase())
        diagnosticData = serializer.getDiagnosticDataDictById(patientId)
        verticalMovementData = diagnosticData["VerticalMandibleMovements"]

        rightSideMm = verticalMovementData["right_side_mm"]
        leftSideMm = verticalMovementData["left_side_mm"]
        forwardMm = verticalMovementData["forward_mm"]

        rightSideRight = verticalMovementData["right_side_right"]
        leftSideRight = verticalMovementData["left_side_right"]
        forwardRight = verticalMovementData["forward_right"]

        rightSideLeft = verticalMovementData["right_side_left"]
        leftSideLeft = verticalMovementData["left_side_left"]
        forwardLeft = verticalMovementData["forward_left"]

        self.mm.getLineEdit("Right side").setText(rightSideMm)
        self.mm.getLineEdit("Left side").setText(leftSideMm)
        self.mm.getLineEdit("Forward").setText(forwardMm)

        rightOptions = self.painOptions.getRightOptions().getOptions()
        rightOptions["Right side"].getButton(rightSideRight).setChecked(True)
        rightOptions["Left side"].getButton(leftSideRight).setChecked(True)
        rightOptions["Forward"].getButton(forwardRight).setChecked(True)

        leftOptions = self.painOptions.getLeftOptions().getOptions()
        leftOptions["Right side"].getButton(rightSideLeft).setChecked(True)
        leftOptions["Left side"].getButton(leftSideLeft).setChecked(True)
        leftOptions["Forward"].getButton(forwardLeft).setChecked(True)
