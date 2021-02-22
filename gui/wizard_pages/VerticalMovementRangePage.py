from gui.wizard_pages.BaseWizardPage import PageWithSideOptions
from gui.wizard_pages.WizardPagesHelpers import *
from algo.DatabaseDeserializer import DatabaseDeserializer


class VerticalMovementRangePage(PageWithSideOptions):
    def __init__(self):
        super().__init__()
        self.setTitle("3. Vertical movement range")

        self.usedForetooth = ButtonGroupBox("Used foretooth", ["11", "21"], layout='horizontal')
        self.registerField("Used foretooth", self.usedForetooth,
                           property="checkedButton",
                           changedSignal=self.usedForetooth.buttonClicked, mandatory=True)
        self.usedForetooth.getWidget().setFont(self.defaultFont)

        self.mm = MmInputs(["No pain opening", "Max active opening", "Max passive opening"], "mm", self.defaultFont)

        mmLineEdits = self.mm.getAllLineEdits()
        for lineEditName in mmLineEdits:
            self.registerField(mmLineEdits[lineEditName].objectName(), mmLineEdits[lineEditName], mandatory=True)

        rightLayout = QHBoxLayout()
        self.painOptions = SideOptions(["Max active opening", "Max passive opening"],
                                       ["None", "Muscle", "Joint", "Both"], self.defaultFont)
        self.registerSideOptions(isMandatory=True)

        rightLayout.addLayout(self.painOptions.getLayout())
        mainLayout = QGridLayout()

        mainLayout.addWidget(self.usedForetooth.getWidget(), 0, 0)
        mainLayout.addWidget(self.mm.getWidget(), 1, 0)
        mainLayout.addLayout(rightLayout, 1, 1)
        self.setLayout(mainLayout)

    def clearAll(self):
        self.painOptions.clearAll()
        self.usedForetooth.clearAll()

    def doLoadWithData(self, patientId):
        serializer = DatabaseDeserializer(self.wizard().getDatabase())
        diagnosticData = serializer.getDiagnosticDataDictById(patientId)
        verticalMovementRangeData = diagnosticData["VerticalMovementRange"]

        usedForetooth = verticalMovementRangeData["used_foretooth"]

        noPainOpening = verticalMovementRangeData["no_pain_opening_mm"]
        maxActiveOpening = verticalMovementRangeData["max_active_opening_mm"]
        maxPassiveOpening = verticalMovementRangeData["max_passive_opening_mm"]

        maxActiveOpeningRight = verticalMovementRangeData["max_active_opening_right"]
        maxPassiveOpeningRight = verticalMovementRangeData["max_passive_opening_right"]
        maxActiveOpeningLeft = verticalMovementRangeData["max_active_opening_left"]
        maxPassiveOpeningLeft = verticalMovementRangeData["max_passive_opening_left"]

        self.usedForetooth.getButton(usedForetooth).setChecked(True)

        self.mm.getLineEdit("No pain opening").setText(noPainOpening)
        self.mm.getLineEdit("Max active opening").setText(maxActiveOpening)
        self.mm.getLineEdit("Max passive opening").setText(maxPassiveOpening)

        rightOptions = self.painOptions.getRightOptions().getOptions()
        rightOptions["Max active opening"].getButton(maxActiveOpeningRight).setChecked(True)
        rightOptions["Max passive opening"].getButton(maxPassiveOpeningRight).setChecked(True)

        leftOptions = self.painOptions.getLeftOptions().getOptions()
        leftOptions["Max active opening"].getButton(maxActiveOpeningLeft).setChecked(True)
        leftOptions["Max passive opening"].getButton(maxPassiveOpeningLeft).setChecked(True)
