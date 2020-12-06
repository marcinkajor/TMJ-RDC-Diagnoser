from gui.wizard_pages.BaseWizardPage import BasePage
from gui.wizard_pages.WizardPagesHelpers import *
from PyQt5.QtGui import QFont


class MusclesAndJointPalpationPainPage(BasePage):
    def __init__(self, database):
        super(BasePage, self).__init__()
        self.setTitle("7. Muscles & joint palpation pain")
        self.database = database

        self.painOptions = SideOptions(["Mastoid process (lateral upper part)", "Frontal (pupil line, beneath hair))",
                                        "Vertex (1 cm lateral from skull prominence)"],
                                       ["None", "Subtle", "Moderate", "Strong"], self.defaultFont, "BKD protocol")

        additionalInfo = QLabel("No pain areas")
        additionalInfo.setFont(QFont("Arial", 11, QFont.Bold))

        rightLayout = QHBoxLayout()
        rightLayout.addLayout(self.painOptions.getLayout())
        mainLayout = QGridLayout()
        mainLayout.addWidget(additionalInfo, 0, 0)
        mainLayout.addLayout(rightLayout, 1, 0)
        self.setLayout(mainLayout)

