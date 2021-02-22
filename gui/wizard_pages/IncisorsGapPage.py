from gui.wizard_pages.BaseWizardPage import BasePage
from gui.wizard_pages.WizardPagesHelpers import *
from algo.DatabaseDeserializer import DatabaseDeserializer


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

    def doLoadWithData(self, patientId):
        serializer = DatabaseDeserializer(self.wizard().getDatabase())
        diagnosticData = serializer.getDiagnosticDataDictById(patientId)
        incisorsGap = diagnosticData["IncisorsGap"]

        verticalMm = incisorsGap["vertical_mm"]
        horizontalMm = incisorsGap["horizontal_mm"]
        middleLineMm = incisorsGap["middle_line_mm"]
        middleLineRelative = incisorsGap["middle_line_alignment_relative_to_the_jaw"]

        self.mm.getLineEdit("Vertical").setText(verticalMm)
        self.mm.getLineEdit("Horizontal").setText(horizontalMm)
        self.mm.getLineEdit("Middle line").setText(middleLineMm)
        self.middleLineAlignment.getButton(middleLineRelative).setChecked(True)
