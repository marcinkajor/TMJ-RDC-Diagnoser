from gui.wizard_pages.BaseWizardPage import BasePage
from gui.wizard_pages.WizardPagesHelpers import *
from algo.DatabaseDeserializer import DatabaseDeserializer
from PyQt5.QtGui import QFont


class QuestionnairePage(BasePage):
    def __init__(self):
        super().__init__()

        self.setTitle("Questionnaire 1")
        self.layout = QVBoxLayout()
        self.label1 = QLabel("Has the patient had pain in the face, jaw, temple, in front of the ear "
                             "or in the ear in the past month?")
        font = QFont("Arial", 10, QFont.Bold)
        self.label1.setFont(font)
        self.painSymptomsBox = ButtonGroupBox("Pain symptoms", ["Yes", "No"], layout='horizontal')
        self.registerField("Pain symptoms", self.painSymptomsBox,
                           property="checkedButton",
                           changedSignal=self.painSymptomsBox.buttonClicked, mandatory=True)
        self.painSymptomsBox.getWidget().setFont(self.defaultFont)

        self.label2 = QLabel("Has the patient ever had jaw lock or catch so that it won't open all the way?")
        self.label2.setFont(font)
        self.openingProblemsBox = ButtonGroupBox("Opening problems", ["Yes", "No"], layout='horizontal')
        self.registerField("Opening problems", self.openingProblemsBox,
                           property="checkedButton",
                           changedSignal=self.openingProblemsBox.buttonClicked, mandatory=True)
        self.openingProblemsBox.getWidget().setFont(self.defaultFont)

        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.painSymptomsBox.getWidget())
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.openingProblemsBox.getWidget())
        self.layout.setSpacing(25)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def clearAll(self):
        self.painSymptomsBox.clearAll()
        self.openingProblemsBox.clearAll()

    def doLoadWithData(self, patientId):
        serializer = DatabaseDeserializer(self.wizard().getDatabase())
        diagnosticData = serializer.getDiagnosticDataDictById(patientId)
        questionnaire = diagnosticData["Questionnaire"]
        painSymptoms = questionnaire["pain_symptoms"]
        openingProblems = questionnaire["opening_problems"]

        self.painSymptomsBox.getButton(painSymptoms).setChecked(True)
        self.openingProblemsBox.getButton(openingProblems).setChecked(True)
