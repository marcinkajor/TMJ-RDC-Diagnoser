from PyQt5.QtWidgets import QGroupBox, QRadioButton, QVBoxLayout, QButtonGroup, QWidget, QHBoxLayout, \
    QLabel, QLineEdit, QGridLayout
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import pyqtSignal, pyqtProperty


class ButtonGroupBox(QWidget):

    buttonClicked = pyqtSignal()

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
        self.buttonGroup.buttonClicked.connect(self.onButtonClicked)

    def getWidget(self):
        return self.box

    def enableAll(self, enable):
        assert(enable in [True, False])
        for button in self.buttonGroup.buttons():
            button.setEnabled(enable)

    def clearAll(self):
        self.buttonGroup.setExclusive(False)
        for button in self.buttonGroup.buttons():
            if button.isChecked():
                button.setChecked(False)
        self.buttonGroup.setExclusive(True)

    def getButton(self, name):
        assert(name in self.buttonNames)
        for button in self.buttonGroup.buttons():
            if button.objectName() == name:
                return button

    def registerClickCallback(self, callback):
        self.buttonGroup.buttonClicked.connect(callback)

    @pyqtProperty(str, notify=buttonClicked)
    def checkedButton(self):
        if self.buttonGroup.checkedButton():
            return self.buttonGroup.checkedButton().objectName()

    def onButtonClicked(self, buttonId):
        self.buttonClicked.emit()


class MmInputs:
    def __init__(self, inputs, font):
        mmValidator = QIntValidator(0, 9999)
        self.inputs = {}
        self.layout = QGridLayout()
        self.mmBox = QGroupBox("mm")

        for idx, mmInput in enumerate(inputs):
            label = QLabel(mmInput)
            self.inputs[mmInput] = QLineEdit()
            self.inputs[mmInput].setValidator(mmValidator)
            self.layout.addWidget(label, idx, 0)
            self.layout.addWidget(self.inputs[mmInput], idx, 1)

        self.mmBox.setLayout(self.layout)
        self.mmBox.setFont(font)

    def getLineEdit(self, name):
        return self.inputs[name]

    def getAllLineEdits(self):
        return self.inputs

    def getWidget(self):
        return self.mmBox
