from PyQt5 import QtGui
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtWidgets import QLineEdit, QWizardPage, QLabel, QGroupBox, QRadioButton, QVBoxLayout, QGridLayout


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
