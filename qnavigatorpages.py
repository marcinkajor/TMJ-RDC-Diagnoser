from PyQt5 import QtGui
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtWidgets import QLineEdit, QWizardPage, QLabel, QGridLayout
from qnavigatorpageshelper import *


class BasePage(QWizardPage):
    def __init__(self):
        super(QWizardPage, self).__init__()
        self.setWindowIcon(QtGui.QIcon('tooth.png'))

    def onNextClicked(self):
        pass


class PersonalDataPage(BasePage):
    def __init__(self, database):
        super(BasePage, self).__init__()
        self.database = database
        self.setTitle("Personal patient data")
        # generate all needed QLineEdits with corresponding validators
        self.formItems = self._generateForm([("Name", None), ("Surname", None), ("Age", QIntValidator(18, 120))])
        self.vboxLayout = QVBoxLayout()
        for formItemName in self.formItems:
            self.vboxLayout.addWidget(QLabel(formItemName))
            self.vboxLayout.addWidget(self.formItems[formItemName])
        self.sexButtonGroup = ButtonGroupBox("Sex", ["Male", "Female"], layout='vertical')
        self.registerField("Sex", self.sexButtonGroup,
                           property="checkedButton",  # This is a property defined in ButtonGroupBox!!
                           changedSignal=self.sexButtonGroup.buttonClicked)
        self.vboxLayout.addWidget(self.sexButtonGroup.getWidget())

        self.setLayout(self.vboxLayout)

    def _generateForm(self, listOfItemsAndValidators):
        formItems = {}
        for item in listOfItemsAndValidators:
            name = item[0]
            validator = item[1]
            newLineEdit = QLineEdit()
            newLineEdit.setObjectName(name)
            newLineEdit.setValidator(validator)
            newLineEdit.setFont(QFont("Arial", 14))
            formItems[item[0]] = newLineEdit
            self.registerField(name, newLineEdit)
        return formItems

    def onNextClicked(self):
        try:
            self.database.addNewPatientRecord(
                (self.formItems["Name"].text(), self.formItems["Surname"].text(), self.formItems["Age"].text(), "MALE"))
        except Exception as e:
            print(e)


class InitialDataPage(BasePage):
    def __init__(self, database):
        super(BasePage, self).__init__()

        self.database = database
        self.NO_PAIN = "NO PAIN"
        self.RIGHT = "RIGHT"
        self.LEFT = "LEFT"
        self.BOTH = "BOTH"

        self.setTitle("1. Initial patient interview")
        self.grid = QGridLayout()
        self.painSideBox = ButtonGroupBox("Pain side", [self.NO_PAIN, self.RIGHT, self.LEFT, self.BOTH],
                                          layout='horizontal')
        self.painSideBox.registerClickCallback(self._onButtonGroupChanged)

        self.painAreaBox = self._generatePainOptions()

        self.majorBox = QGroupBox("Facial pain")
        self.majorBox.setFont(QFont("Arial", 10))
        vLayout = QVBoxLayout()
        vLayout.addWidget(self.painSideBox.getWidget())
        vLayout.addWidget(self.painAreaBox)
        self.majorBox.setLayout(vLayout)
        self.grid.addWidget(self.majorBox)
        self.setLayout(self.grid)

    def _onButtonGroupChanged(self):
        print("Sex: {}".format(self.field("Sex")))  # TODO: Remove, only for testing custom field
        currentOption = self.painSideBox.checkedButton
        if currentOption is None:
            return
        if currentOption != self.NO_PAIN:
            self.painSideBox.setEnabled(True)
            if currentOption == self.RIGHT:
                self._enablePainOptions(right=True, left=False)
            elif currentOption == self.LEFT:
                self._enablePainOptions(right=False, left=True)
            else:
                self._enablePainOptions(right=True, left=True)
        else:
            self._enablePainOptions(left=False, right=False)

    def _enablePainOptions(self, right, left):
        self.rightOptionsGroup.enableAll(right)
        self.leftOptionsGroup.enableAll(left)

    def _generatePainOptions(self):
        options = ["Muscle", "Join", "Both"]
        self.optionsGridLayout = QHBoxLayout()
        self.rightOptionsGroup = ButtonGroupBox("Right", options, layout='horizontal')
        self.leftOptionsGroup = ButtonGroupBox("Left", options, layout='horizontal')
        self.optionsGridLayout.addWidget(self.rightOptionsGroup.getWidget())
        self.optionsGridLayout.addWidget(self.leftOptionsGroup.getWidget())
        self._enablePainOptions(right=False, left=False)
        self.painAreaBox = QGroupBox("Pain area")
        self.painAreaBox.setLayout(self.optionsGridLayout)
        return self.painAreaBox


class AbductionMovementPage(BasePage):
    def __init__(self, database):
        super(BasePage, self).__init__()
        self.setTitle("2. Abduction movement")

        self.movementBox = ButtonGroupBox("Abduction movement", ["Straight",
                                                                 "Uncorrected Right Deviation",
                                                                 ''''S' left corrected deviation'''],
                                          layout="vertical")
        layout = QVBoxLayout()
        layout.addWidget(self.movementBox.getWidget())
        self.setLayout(layout)
