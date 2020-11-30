from PyQt5 import QtGui
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtWidgets import QLineEdit, QWizardPage, QLabel, QGridLayout
from qnavigatorpageshelper import *


class BasePage(QWizardPage):
    defaultFont = QFont("Arial", 10)

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
        self.majorBox.setFont(self.defaultFont)
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
        if right and not left:
            self.leftOptionsGroup.clearAll()
        if left and not right:
            self.rightOptionsGroup.clearAll()
        if not left and not right:
            self.rightOptionsGroup.clearAll()
            self.leftOptionsGroup.clearAll()
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

    Mapping = {
        "Straight": 0,
        "Uncorrected right deviation": 1,
        "'S' left corrected deviation": 2,
        "Non-corrected left deviation": 3,
        "'S' left corrected deviation": 4,
        "Other": 5
    }

    def __init__(self, database):
        super(BasePage, self).__init__()
        self.setTitle("2. Abduction movement")

        self.movementBox = ButtonGroupBox("Abduction movement", self.Mapping.keys(), layout="vertical")
        self.otherDescription = QLineEdit()
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
        currentOption = self.movementBox.checkedButton
        if currentOption is None:
            return
        if currentOption == "Other":
            self.otherDescription.setEnabled(True)
        else:
            self.otherDescription.clear()
            self.otherDescription.setEnabled(False)


class VerticalMovementRangePage(BasePage):
    def __init__(self, database):
        super(BasePage, self).__init__()
        self.setTitle("3. Vertical movement range")
        self.database = database

        self.usedForetooth = ButtonGroupBox("Used foretooth", ["11", "21"], layout='horizontal')
        self.usedForetooth.getWidget().setFont(self.defaultFont)

        mmValidator = QIntValidator(0, 9999)

        self.noPainOpeningLabel = QLabel("No pain opening")
        self.noPainOpeningValue = QLineEdit()
        self.noPainOpeningValue.setValidator(mmValidator)

        self.maxActiveOpeningLabel = QLabel("Max active opening")
        self.maxPassiveOpeningValue = QLineEdit()
        self.maxPassiveOpeningValue.setValidator(mmValidator)

        self.maxPassiveOpeningLabel = QLabel("Max passive opening")
        self.maxActiveOpeningValue = QLineEdit()
        self.maxActiveOpeningValue.setValidator(mmValidator)

        leftLayout = QGridLayout()
        leftLayout.addWidget(self.noPainOpeningLabel, 0, 0)
        leftLayout.addWidget(self.maxActiveOpeningLabel, 1, 0)
        leftLayout.addWidget(self.maxPassiveOpeningLabel, 2, 0)
        leftLayout.addWidget(self.noPainOpeningValue, 0, 1)
        leftLayout.addWidget(self.maxActiveOpeningValue, 1, 1)
        leftLayout.addWidget(self.maxPassiveOpeningValue, 2, 1)
        self.mmBox = QGroupBox("mm")
        self.mmBox.setLayout(leftLayout)
        self.mmBox.setFont(self.defaultFont)

        rightLayout = QHBoxLayout()
        rightLayout.addLayout(self._generatePainOptions())
        mainLayout = QGridLayout()

        mainLayout.addWidget(self.usedForetooth.getWidget(), 0, 0)
        mainLayout.addWidget(self.mmBox, 1, 0)
        mainLayout.addLayout(rightLayout, 1, 1)
        self.setLayout(mainLayout)

    def _generatePainOptions(self):
        options = ["None", "Muscle", "Join", "Both"]
        self.rightOptionsGridLayout = QVBoxLayout()
        self.maxActiveOpenOptGroupRight = ButtonGroupBox("Max active opening", options, layout='horizontal')
        self.maxPassiveOpenOptGroupRight = ButtonGroupBox("Max passive opening", options, layout='horizontal')
        self.rightOptionsGridLayout.addWidget(self.maxActiveOpenOptGroupRight.getWidget())
        self.rightOptionsGridLayout.addWidget(self.maxPassiveOpenOptGroupRight.getWidget())

        self.leftOptionsGridLayout = QVBoxLayout()
        self.maxActiveOpenOptGroupLeft = ButtonGroupBox("Max active opening", options, layout='horizontal')
        self.maxPassiveOpenOptGroupLeft = ButtonGroupBox("Max passive opening", options, layout='horizontal')
        self.leftOptionsGridLayout.addWidget(self.maxActiveOpenOptGroupLeft.getWidget())
        self.leftOptionsGridLayout.addWidget(self.maxPassiveOpenOptGroupLeft.getWidget())

        self.rightPainAreaBox = QGroupBox("Right side pain")
        self.rightPainAreaBox.setFont(self.defaultFont)
        self.leftPainAreaBox = QGroupBox("Left side pain")
        self.leftPainAreaBox.setFont(self.defaultFont)
        self.rightPainAreaBox.setLayout(self.rightOptionsGridLayout)
        self.leftPainAreaBox.setLayout(self.leftOptionsGridLayout)

        finalLayout = QHBoxLayout()
        finalLayout.addWidget(self.rightPainAreaBox)
        finalLayout.addWidget(self.leftPainAreaBox)

        return finalLayout


class IncisorsGapPage(BasePage):
    def __init__(self, database):
        super(BasePage, self).__init__()
        self.setTitle("4. Incisors gap")
        self.database = database

        mmValidator = QIntValidator(0, 9999)

        self.verticalLabel = QLabel("Vertical")
        self.verticalValue = QLineEdit()
        self.verticalValue.setValidator(mmValidator)

        self.horizontalLabel = QLabel("Horizontal")
        self.horizontalValue = QLineEdit()
        self.horizontalValue.setValidator(mmValidator)

        self.middleLineLabel = QLabel("Middle line")
        self.middleLineValue = QLineEdit()
        self.middleLineValue.setValidator(mmValidator)

        leftLayout = QGridLayout()
        leftLayout.addWidget(self.verticalLabel, 0, 0)
        leftLayout.addWidget(self.horizontalLabel, 1, 0)
        leftLayout.addWidget(self.middleLineLabel, 2, 0)
        leftLayout.addWidget(self.verticalValue, 0, 1)
        leftLayout.addWidget(self.horizontalValue, 1, 1)
        leftLayout.addWidget(self.middleLineValue, 2, 1)

        self.mmBox = QGroupBox("mm")
        self.mmBox.setLayout(leftLayout)
        self.mmBox.setFont(self.defaultFont)

        self.middleLineAlignment = ButtonGroupBox("Middle line alignment relative to the jaw", ["R", "L"],
                                                  layout='horizontal')
        self.middleLineAlignment.getWidget().setFont(self.defaultFont)

        rightLayout = QHBoxLayout()
        rightLayout.addWidget(self.middleLineAlignment.getWidget())
        mainLayout = QGridLayout()

        mainLayout.addWidget(self.mmBox, 0, 0)
        mainLayout.addLayout(rightLayout, 0, 1)
        self.setLayout(mainLayout)
