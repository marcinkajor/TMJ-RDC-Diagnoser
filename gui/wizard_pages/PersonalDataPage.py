from gui.wizard_pages.BaseWizardPage import BasePage
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
from gui.wizard_pages.WizardPagesHelpers import *


'''
Fields:
    - "PersonalDataPage/Name"
    - "PersonalDataPage/Surname"
    - "PersonalDataPage/Age"
    - "PersonalDataPage/Sex"
'''


class PersonalDataPage(BasePage):
    def __init__(self):
        super().__init__()
        self.setTitle("Personal patient data")
        # generate all needed QLineEdits with corresponding validators
        self.formItems = self._generateForm([("Name", None), ("Surname", None), ("Age", QIntValidator(18, 120)),
                                             ("PESEL", QRegExpValidator(QRegExp("^\d{11}$")))])
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
        pass

    def clearAll(self):
        self.sexButtonGroup.clearAll()
