from PyQt5 import QtGui
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtWidgets import QLineEdit, QWizardPage, QLabel, QGroupBox, QVBoxLayout, QGridLayout, QHBoxLayout
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
        self.vboxLayout.addWidget(self._generateSex())
        self.setLayout(self.vboxLayout)

    @staticmethod
    def _generateForm(listOfItemsAndValidators):
        formItems = {}
        for item in listOfItemsAndValidators:
            newLineEdit = QLineEdit()
            newLineEdit.setObjectName(item[0])
            newLineEdit.setValidator(item[1])
            newLineEdit.setFont(QFont("Arial", 12))
            formItems[item[0]] = newLineEdit
        return formItems

    @staticmethod
    def _generateSex():
        return ButtonGroupBox("Sex", ["Male", "Female"], layout='vertical').getWidget()

    def onNextClicked(self):
        try:
            self.database.addNewPatientRecord(
                (self.formItems["Name"].text(), self.formItems["Surname"].text(), self.formItems["Age"].text(), "MALE"))
        except Exception as e:
            print(e)


class InitialDataPage(BasePage):
    def __init__(self, database):
        self.database = database
        self.NO_PAIN = "NO PAIN"
        self.RIGHT = "RIGHT"
        self.LEFT = "LEFT"
        self.BOTH = "BOTH"

        super(BasePage, self).__init__()
        self.setTitle("Initial data page")

        self.grid = QGridLayout()
        self.facialPainBox = ButtonGroupBox("Facial pain", [self.NO_PAIN, self.RIGHT, self.LEFT, self.BOTH],
                                            layout='horizontal')
        self.facialPainBox.registerClickCallback(self._onButtonGroupChanged)
        self.grid.addWidget(self.facialPainBox.getWidget())

        self._generatePainOptions()
        self.setLayout(self.grid)

    def _onButtonGroupChanged(self):
        currentOption = self.facialPainBox.getCheckedButton()
        if currentOption is None:
            return
        if currentOption != self.NO_PAIN:
            self.facialPainBox.setEnabled(True)
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
        self.grid.addWidget(self.painAreaBox)
