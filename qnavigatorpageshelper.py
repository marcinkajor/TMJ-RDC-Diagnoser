from PyQt5.QtWidgets import QGroupBox, QRadioButton, QVBoxLayout, QButtonGroup, QWidget, QHBoxLayout


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
