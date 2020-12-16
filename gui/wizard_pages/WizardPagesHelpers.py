from PyQt5.QtWidgets import QGroupBox, QRadioButton, QVBoxLayout, QButtonGroup, QWidget, QHBoxLayout, \
    QLabel, QLineEdit, QGridLayout
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import pyqtSignal, pyqtProperty


class ButtonGroupBox(QWidget):

    buttonClicked = pyqtSignal()

    def __init__(self, name, buttons, layout='vertical'):
        super().__init__()
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

    def getName(self):
        return self.box.title()


class MmInputs:
    def __init__(self, inputs, name, font):
        mmValidator = QIntValidator(0, 9999)
        self.inputs = {}
        self.layout = QGridLayout()
        self.mmBox = QGroupBox(name)

        for idx, mmInput in enumerate(inputs):
            label = QLabel(mmInput)
            self.inputs[mmInput] = QLineEdit()
            self.inputs[mmInput].setObjectName(mmInput + ' mm')  # make the name unique by adding 'mm'
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


class Options:
    def __init__(self, name, movements, options, font):
        self.options = {}
        self.layout = QVBoxLayout()
        self.boxArea = QGroupBox(name)
        self.boxArea.setFont(font)
        self.mainLayout = QHBoxLayout()

        for move in movements:
            groupBox = ButtonGroupBox(move, options, layout='horizontal')
            self.options[move] = groupBox
            self.layout.addWidget(groupBox.getWidget())

        self.boxArea.setLayout(self.layout)

        self.mainLayout.addWidget(self.boxArea)

    def getLayout(self):
        return self.mainLayout

    def getOptions(self):
        return self.options


class SideOptions:
    def __init__(self,  movements, options, font, additionalInfo=None):
        rightLabel = "Right side pain ({})".format(additionalInfo) if additionalInfo else "Right side pain"
        leftLabel = "Left side pain ({})".format(additionalInfo) if additionalInfo else "Left side pain"
        self.rightOptions = None
        self.leftOptions = None
        self.mainLayout = None
        if movements and options and font:
            self.rightOptions = Options(rightLabel, movements, options, font)
            self.leftOptions = Options(leftLabel, movements, options, font)
            self.mainLayout = QHBoxLayout()
            self.mainLayout.addLayout(self.rightOptions.getLayout())
            self.mainLayout.addLayout(self.leftOptions.getLayout())

    def __bool__(self):
        return self.rightOptions is not None and self.leftOptions is not None and self.mainLayout is not None

    def getLayout(self):
        return self.mainLayout

    def getRightOptions(self):
        return self.rightOptions

    def getLeftOptions(self):
        return self.leftOptions
