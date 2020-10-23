from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWizard, QLineEdit, QWizardPage, QLabel, QFormLayout


class PersonalDataPage(QWizardPage):
    def __init__(self):
        super(PersonalDataPage, self).__init__()
        self.setTitle("Personal patient data")
        self.setWindowIcon(QtGui.QIcon('tooth.png'))
        self.formItems = self._generateForm()
        self.form = QFormLayout()
        for formItemName in self.formItems:
            self.form.addRow(QLabel(formItemName))
            self.form.addRow(self.formItems[formItemName])
        self.setLayout(self.form)

    @staticmethod
    def _generateForm():
        formItemNames = ["Name", "Surname", "Age"]
        formItems = {}
        for formItemName in formItemNames:
            newFormItem = QLineEdit()
            newFormItem.setFont(QFont("Arial", 12))
            newFormItem.setObjectName(formItemName)
            formItems[formItemName] = newFormItem
        return formItems

    def onNameChanged(self, name):
        pass  # TODO: this is rather not necessary, the NEXT button shall trigger proper input data handling
