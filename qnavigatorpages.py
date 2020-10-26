from PyQt5 import QtGui
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtWidgets import QLineEdit, QWizardPage, QLabel, QGroupBox, QRadioButton, QVBoxLayout, QGridLayout, \
    QButtonGroup, QWidget, QHBoxLayout


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
        return ButtonGroupBox("Sex", ["Male", "Female"], layout='vertical').getWidget()

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


class ButtonGroupBox(QWidget):
    def __init__(self, name, buttons, layout='vertical'):
        super(ButtonGroupBox, self).__init__()
        assert(layout in ['vertical', 'horizontal'])
        layout = QVBoxLayout() if layout == 'vertical' else QHBoxLayout()
        self.buttonGroup = QButtonGroup()
        self.box = QGroupBox(name)
        self.buttonNames = []
        for buttonId, buttonName in enumerate(buttons):
            newButton = QRadioButton(buttonName)
            newButton.setObjectName(buttonName)
            self.buttonNames.append(buttonName)
            self.buttonGroup.addButton(newButton, buttonId)
            layout.addWidget(newButton)
        self.box.setLayout(layout)

    def getWidget(self):
        return self.box

    def enableAll(self, enable):
        assert(enable in [True, False])
        for button in self.buttonGroup.buttons():
            button.setEnabled(enable)

    def getButton(self, name):
        assert(name in self.buttonNames)
        for button in self.buttonGroup.buttons():
            if button.objectName() == name:
                return button

    def registerClickCallback(self, callback):
        self.buttonGroup.buttonClicked.connect(callback)

    def getCheckedButton(self):
        if self.buttonGroup.checkedButton():
            return self.buttonGroup.checkedButton().objectName()
