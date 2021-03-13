from gui.wizard_pages.BaseWizardPage import BasePage
from gui.wizard_pages.WizardPagesHelpers import *
from algo.DatabaseDeserializer import DatabaseDeserializer
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollArea, QScrollBar


class QuestionnairePage2(BasePage):
    def __init__(self):
        super().__init__()

        self.setTitle("Questionnaire 2")
        scoreItems = [str(x) for x in range(0, 11)]

        self.label1 = QLabel('''How would patient rate facial pain on a 0 to 10 scale at the present time, that is
right now, where 0 is "no pain" and 10 is "pain as bad as could be"?''')
        font = QFont("Arial", 10, QFont.Bold)
        self.label1.setFont(font)
        self.facialPainScoreSymptomsBox = ButtonGroupBox("Facial pain score", scoreItems, layout='horizontal')
        self.registerField("Facial pain score", self.facialPainScoreSymptomsBox,
                           property="checkedButton",
                           changedSignal=self.facialPainScoreSymptomsBox.buttonClicked, mandatory=True)
        self.facialPainScoreSymptomsBox.getWidget().setFont(self.defaultFont)

        self.label2 = QLabel('''In the past six months, how intense was worst pain rated on a 0 to 10 scale
where 0 is "no pain" and 10 is "pain as bad as could be"?''')
        self.label2.setFont(font)
        self.worstPainScoreBox = ButtonGroupBox("Worst pain score", scoreItems, layout='horizontal')
        self.registerField("Worst pain score", self.worstPainScoreBox,
                           property="checkedButton",
                           changedSignal=self.worstPainScoreBox.buttonClicked, mandatory=True)
        self.worstPainScoreBox.getWidget().setFont(self.defaultFont)

        self.label3 = QLabel('''In the past six months, on the average, how intense was patient's pain rated on a
0 to 10 scale where 0 is "no pain" and 10 is "pain as bad as could be"?''')
        self.label3.setFont(font)
        self.averagePainScoreBox = ButtonGroupBox("Average pain score", scoreItems, layout='horizontal')
        self.registerField("Average pain score", self.averagePainScoreBox,
                           property="checkedButton",
                           changedSignal=self.averagePainScoreBox.buttonClicked, mandatory=True)
        self.averagePainScoreBox.getWidget().setFont(self.defaultFont)

        self.label4 = QLabel('''About how many days in the last six months has patient been kept from usual
activities (work, school or housework) because of facial pain?''')
        self.label4.setFont(font)
        self.daysLineEdit = QLineEdit()
        self.daysLineEdit.setValidator(QIntValidator(0, 999999))
        self.registerField("Days without activities", self.daysLineEdit, mandatory=True)

        self.label5 = QLabel('''In the past six months, how much has facial pain interfered with patient's daily activities
rated on a 0 to 10 scale where 0 is "no interference" and 10 is "unable to carry on any activities"?''')
        self.label5.setFont(font)
        self.sixMonthsInterferencePainScoreBox = ButtonGroupBox("Six months pain interference", scoreItems,
                                                                layout='horizontal')
        self.registerField("Six months pain interference", self.sixMonthsInterferencePainScoreBox,
                           property="checkedButton",
                           changedSignal=self.sixMonthsInterferencePainScoreBox.buttonClicked, mandatory=True)
        self.sixMonthsInterferencePainScoreBox.getWidget().setFont(self.defaultFont)

        self.label6 = QLabel('''In the past six months, how much has facial pain changed patient's ability to take part
in recreational, social and family activities where 0 is "no interference " and 10 is "extreme change"?''')
        self.label6.setFont(font)
        self.sixMonthsChangeRecreationPainScoreBox = ButtonGroupBox("Six months pain recreation change", scoreItems,
                                                                    layout='horizontal')
        self.registerField("Six months pain recreation change", self.sixMonthsChangeRecreationPainScoreBox,
                           property="checkedButton",
                           changedSignal=self.sixMonthsChangeRecreationPainScoreBox.buttonClicked, mandatory=True)
        self.sixMonthsChangeRecreationPainScoreBox.getWidget().setFont(self.defaultFont)

        self.label7 = QLabel('''In the past six months, how much has facial pain changed patient's ability to work
including housework) where 0 is "no interference " and 10 is "extreme change"?''')
        self.label7.setFont(font)
        self.sixMonthsChangeWorkAbilityPainScoreBox = ButtonGroupBox("Six months pain work ability change", scoreItems,
                                                                     layout='horizontal')
        self.registerField("Six months pain work ability change", self.sixMonthsChangeWorkAbilityPainScoreBox,
                           property="checkedButton",
                           changedSignal=self.sixMonthsChangeWorkAbilityPainScoreBox.buttonClicked, mandatory=True)
        self.sixMonthsChangeWorkAbilityPainScoreBox.getWidget().setFont(self.defaultFont)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.facialPainScoreSymptomsBox.getWidget())
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.worstPainScoreBox.getWidget())
        self.layout.addWidget(self.label3)
        self.layout.addWidget(self.averagePainScoreBox.getWidget())
        self.layout.addWidget(self.label4)
        self.layout.addWidget(self.daysLineEdit)
        self.layout.addWidget(self.label5)
        self.layout.addWidget(self.sixMonthsInterferencePainScoreBox.getWidget())
        self.layout.addWidget(self.label6)
        self.layout.addWidget(self.sixMonthsChangeRecreationPainScoreBox.getWidget())
        self.layout.addWidget(self.label7)
        self.layout.addWidget(self.sixMonthsChangeWorkAbilityPainScoreBox.getWidget())
        self.layout.setSpacing(25)
        self.layout.addStretch()

        self.scrollArea = QScrollArea()
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.scrollArea)
        self.mainWidget.setLayout(self.layout)
        self.scrollArea.setWidget(self.mainWidget)

        self.setLayout(self.mainLayout)

    def clearAll(self):
        self.facialPainScoreSymptomsBox.clearAll()
        self.worstPainScoreBox.clearAll()

    def doLoadWithData(self, patientId):
        pass
        # serializer = DatabaseDeserializer(self.wizard().getDatabase())
        # diagnosticData = serializer.getDiagnosticDataDictById(patientId)
        # questionnaire = diagnosticData["Questionnaire"]
        # painSymptoms = questionnaire["pain_symptoms"]
        # openingProblems = questionnaire["opening_problems"]
        #
        # self.painSymptomsBox.getButton(painSymptoms).setChecked(True)
        # self.openingProblemsBox.getButton(openingProblems).setChecked(True)
