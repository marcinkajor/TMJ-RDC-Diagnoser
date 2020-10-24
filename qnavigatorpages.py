from PyQt5 import QtGui
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtWidgets import QLineEdit, QWizardPage, QLabel, QGroupBox, QRadioButton, QVBoxLayout, QGridLayout, \
    QButtonGroup, QWidget


class PersonalDataPage(QWizardPage):
    def __init__(self):
        super(PersonalDataPage, self).__init__()
        self.setTitle("Personal patient data")
        self.setWindowIcon(QtGui.QIcon('tooth.png'))
        # generate all needed QLineEdits with corresponding validators
        self.formItems = self._generateForm([("Name", None), ("Surname", None), ("Age", QIntValidator(18, 120))])
        self.vboxLayout = QVBoxLayout()
        for formItemName in self.formItems:
            self.vboxLayout.addWidget(QLabel(formItemName))
            self.vboxLayout.addWidget(self.formItems[formItemName])
        self.vboxLayout.addWidget(self._generateSex())
        self.setLayout(self.vboxLayout)

    @staticmethod
    def _generateForm(listOfItemsAndValidators):
        formItems = {}
        for item in listOfItemsAndValidators:
            newLineEdit = QLineEdit()
            newLineEdit.setValidator(item[1])
            newLineEdit.setFont(QFont("Arial", 12))
            formItems[item[0]] = newLineEdit
        return formItems

    @staticmethod
    def _generateSex():
        box = QGroupBox("Sex")
        male = QRadioButton("Male")
        female = QRadioButton("Female")
        male.setChecked(True)
        layout = QVBoxLayout()
        layout.addWidget(male)
        layout.addWidget(female)
        box.setLayout(layout)
        return box

    def onNameChanged(self, name):
        pass  # TODO: this is rather not necessary, the NEXT button shall trigger proper input data handling


class InitialDataPage(QWizardPage):
    def __init__(self):
        self.NO_PAIN = "NO PAIN"
        self.RIGHT = "RIGHT"
        self.LEFT = "LEFT"
        self.BOTH = "BOTH"

        super(InitialDataPage, self).__init__()
        self.setTitle("Initial data page")
        self.setWindowIcon(QtGui.QIcon('tooth.png'))

        self.grid = QGridLayout()
        self.labelPresence = QLabel("Facial pain")
        self.labelPresence.setFont(QFont("Arial", 12))
        self.labelArea = QLabel("Pain area")
        self.labelArea.setFont(QFont("Arial", 12))
        self.grid.addWidget(self.labelPresence)
        self.grid.addWidget(self.labelArea)
        self.facialPainState = [self.NO_PAIN, self.RIGHT, self.LEFT, self.BOTH]
        self._generateSideLocalizationButtonGroup(self.facialPainState)
        self._generatePainOptions()
        self.setLayout(self.grid)

    def _generateSideLocalizationButtonGroup(self, options):
        self.buttonGroup = QButtonGroup()
        for buttonId, option in enumerate(options):
            newRadioButton = QRadioButton(option)
            newRadioButton.setObjectName(option)
            self.buttonGroup.addButton(newRadioButton, buttonId)
            self.grid.addWidget(newRadioButton, 0, buttonId + 1)  # +1 to avoid overlapping with QLabel at (0,0)
        self.buttonGroup.buttonClicked.connect(self._onButtonGroupChanged)

    def _onButtonGroupChanged(self):
        currentOption = self.buttonGroup.checkedButton().objectName()
        if currentOption != self.NO_PAIN:
            self.optionsGridLayout.setEnabled(True)
            if currentOption == self.RIGHT:
                self._enableOptions(right=True, left=False)
            elif currentOption == self.LEFT:
                self._enableOptions(right=False, left=True)
            else:
                self._enableOptions(right=True, left=True)
        else:
            self._enableOptions(left=False, right=False)

    def _enableOptions(self, right, left):
        for button in self.rightOptionsGroup.buttons():
            button.setEnabled(right)
        for button in self.leftOptionsGroup.buttons():
            button.setEnabled(left)

    def _generatePainOptions(self):
        options = ["Muscle", "Join", "Both"]
        self.optionsGridLayout = QGridLayout()
        self.rightOptionsGroup = QButtonGroup()
        self.leftOptionsGroup = QButtonGroup()
        self.options = QWidget()
        self.optionsGridLayout.addWidget(self.options)

        for buttonId, option in enumerate(options):
            newRightRadioButton = QRadioButton(option)
            newLeftRadioButton = QRadioButton(option)
            self.rightOptionsGroup.addButton(newRightRadioButton, buttonId)
            self.leftOptionsGroup.addButton(newLeftRadioButton, buttonId)
            self.optionsGridLayout.addWidget(newRightRadioButton, buttonId, 0)
            self.optionsGridLayout.addWidget(newLeftRadioButton, buttonId, 1)
        self._enableOptions(right=False, left=False)
        self.grid.addLayout(self.optionsGridLayout, 1, 1)
