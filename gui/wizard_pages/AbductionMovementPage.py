from gui.wizard_pages.BaseWizardPage import BasePage
from gui.wizard_pages.WizardPagesHelpers import *


class AbductionMovementPage(BasePage):
    Mapping = {
        "Straight": 0,
        "Right Lateral Deviation (uncorrected)": 1,
        "Right Corrected ('S') Deviation": 2,
        "Left Lateral Deviation (uncorrected)": 3,
        "Left Corrected ('S') Deviation": 4,
        "Other Type": 5
    }

    def __init__(self):
        super().__init__()
        self.setTitle("2. Abduction movement")

        self.movementBox = ButtonGroupBox("Abduction movement", self.Mapping.keys(), layout="vertical")
        self.registerField("Abduction movement", self.movementBox,
                           property="checkedButton",
                           changedSignal=self.movementBox.buttonClicked, mandatory=True)

        self.otherDescription = QLineEdit()
        self.registerField("Specific description", self.otherDescription)
        self.otherDescription.setObjectName("Please specify")
        self.otherDescription.setEnabled(False)
        self.movementBox.registerClickCallback(self._onButtonGroupChanged)
        self.otherDescriptionLabel = QLabel(self.otherDescription.objectName())
        self.otherDescriptionLabel.setFont(self.defaultFont)
        layout = QVBoxLayout()
        self.movementBox.getWidget().setFont(self.defaultFont)

        layout.addWidget(self.movementBox.getWidget())
        layout.addWidget(self.otherDescriptionLabel)
        layout.addWidget(self.otherDescription)
        self.setLayout(layout)

    def _onButtonGroupChanged(self):
        # TODO: This signal should be emitted automatically by Qt... but it's not when reentering the wizard
        self.completeChanged.emit()
        currentOption = self.movementBox.checkedButton
        if currentOption is None:
            return
        if currentOption == "Other":
            self.otherDescription.setEnabled(True)
        else:
            self.otherDescription.clear()
            self.otherDescription.setEnabled(False)

    def clearAll(self):
        self.movementBox.clearAll()
        self.otherDescription.setEnabled(False)
