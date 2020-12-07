from gui.wizard_pages.BaseWizardPage import BasePage
from gui.wizard_pages.WizardPagesHelpers import *
from PyQt5.QtGui import QFont

painSeverities = ["No pain", "Mild pain", "Moderate pain", "Severe pain"]


class PalpationPainPage(BasePage):
    def __init__(self, database, options, label):
        super().__init__()
        self.setTitle("7. Muscles & joint palpation pain")
        self.database = database

        self.painOptions = SideOptions(options, painSeverities, self.defaultFont, "BKD protocol")

        additionalInfo = QLabel(label)
        additionalInfo.setFont(QFont("Arial", 11, QFont.Bold))

        rightLayout = QHBoxLayout()
        rightLayout.addLayout(self.painOptions.getLayout())
        mainLayout = QGridLayout()
        mainLayout.addWidget(additionalInfo, 0, 0)
        mainLayout.addLayout(rightLayout, 1, 0)
        self.setLayout(mainLayout)


class PalpationPainNoPainPage(PalpationPainPage):
    def __init__(self, database):
        options = "Mastoid process (lateral upper part)", "Frontal (pupil line, beneath hair))",\
                  "Vertex (1 cm lateral from skull prominence)"
        label = "No pain areas"
        super().__init__(database, options, label)


class PalpationPainExtraoralMusclesPage(PalpationPainPage):
    def __init__(self, database):
        options = ['''Temporalis (posterior) - "Back of temple"''',
                                        '''Temporalis (middle) - "Middle of temple"''',
                                        '''Temporalis (anterior) - "Front of temple"''',
                                        '''Masseter (superior) - "Cheek/under cheekbone"''',
                                        '''Masseter (middle) - "Cheek/side of face"''',
                                        '''Masseter (inferior) - "Cheek/jawline"''',
                                        '''Posterior mandibular region - "Jaw/throat region"''',
                                        '''Submandibular region - "Under chin"''']
        label = "Extraoral muscle pain"
        super().__init__(database, options, label)


class PalpationPainJointPainPage(PalpationPainPage):
    def __init__(self, database):
        options = ['''Lateral pole - "outside"''', '''Posterior attachment - "inside ear"''']
        label = "Joint pain"
        super().__init__(database, options, label)


class PalpationPainIntraoralPainPage(PalpationPainPage):
    def __init__(self, database):
        options = ['''Lateral pterygoid area - "Behind upper molars"''', '''Tendon of temporalis - "Tendon"''']
        label = "Intraoral muscle pain"
        super().__init__(database, options, label)
