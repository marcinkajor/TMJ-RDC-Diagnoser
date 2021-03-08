from gui.wizard_pages.BaseWizardPage import BasePage
from gui.wizard_pages.WizardPagesHelpers import *
from algo.DatabaseDeserializer import DatabaseDeserializer
from PyQt5.QtCore import pyqtSignal, pyqtProperty
from PyQt5.QtWidgets import QPushButton, QFileDialog
from PyQt5.QtGui import QFocusEvent


class LineEdit(QLineEdit):
    focusIn = pyqtSignal()

    def __init__(self):
        super(LineEdit, self).__init__()

    def focusInEvent(self, a0: QFocusEvent) -> None:
        super(LineEdit, self).focusInEvent(a0)
        self.focusIn.emit()


class BlobWidget(QWidget):

    changed = pyqtSignal()

    def __init__(self, description):
        super(BlobWidget, self).__init__()
        self._blob = None
        self.fileName = None
        self.nameWidget = LineEdit()
        self.button = QPushButton(description)
        self.button.clicked.connect(self._onButtonClicked)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.nameWidget)
        self.setLayout(self.layout)
        self.nameWidget.focusIn.connect(self._onFocusIn)
        self.nameWidget.textChanged.connect(self._onTextChanged)

    @pyqtProperty("QVariantMap", notify=changed)
    def file(self):
        return {"name": self.fileName, "blob": self._blob}

    @file.setter
    def file(self, data):
        if data != self._blob:
            self._blob = data
            self.changed.emit()

    def setName(self, name):
        self.fileName = name
        self.nameWidget.setText(name)

    def _onButtonClicked(self):
        fileName, fileFilter = QFileDialog.getOpenFileName(self, 'Open File', filter="Audio file (*.wav)")
        self.fileName = fileName.split('/')[-1]
        self.nameWidget.setText(self.fileName)
        try:
            with open(fileName, 'rb') as file:
                self._blob = file.read()
        except Exception as e:
            print(e)

    def _onTextChanged(self, text: str):
        self.fileName = text

    def _onFocusIn(self):
        pass
        # if self._blob is None:
        #     print("setting readonly true")
        #     self.nameWidget.setReadOnly(True)
        # else:
        #     self.nameWidget.setReadOnly(False)
        #     print("setting readonly false")


class AudioFilesPage(BasePage):
    def __init__(self):
        super().__init__()
        self.setTitle("Audio files")
        self.layout = QVBoxLayout()
        self.audio1 = BlobWidget("Add file 1")
        self.audio2 = BlobWidget("Add file 2")
        self.audio3 = BlobWidget("Add file 3")
        self.audio4 = BlobWidget("Add file 4")
        self.audio5 = BlobWidget("Add file 5")
        self.audio6 = BlobWidget("Add file 6")
        self.audio7 = BlobWidget("Add file 7")
        self.audio8 = BlobWidget("Add file 8")

        self.layout.addWidget(self.audio1)
        self.layout.addWidget(self.audio2)
        self.layout.addWidget(self.audio3)
        self.layout.addWidget(self.audio4)
        self.layout.addWidget(self.audio5)
        self.layout.addWidget(self.audio6)
        self.layout.addWidget(self.audio7)
        self.layout.addWidget(self.audio8)

        self.registerField("Audio1", self.audio1, property="file", changedSignal=self.audio1.changed)
        self.registerField("Audio2", self.audio2, property="file", changedSignal=self.audio2.changed)
        self.registerField("Audio3", self.audio3, property="file", changedSignal=self.audio3.changed)
        self.registerField("Audio4", self.audio4, property="file", changedSignal=self.audio4.changed)
        self.registerField("Audio5", self.audio5, property="file", changedSignal=self.audio5.changed)
        self.registerField("Audio6", self.audio6, property="file", changedSignal=self.audio6.changed)
        self.registerField("Audio7", self.audio7, property="file", changedSignal=self.audio7.changed)
        self.registerField("Audio8", self.audio8, property="file", changedSignal=self.audio8.changed)
        self.setLayout(self.layout)

    def clearAll(self):
        self.audio1.nameWidget.clear()
        self.audio2.nameWidget.clear()
        self.audio3.nameWidget.clear()
        self.audio4.nameWidget.clear()
        self.audio5.nameWidget.clear()
        self.audio6.nameWidget.clear()
        self.audio7.nameWidget.clear()
        self.audio8.nameWidget.clear()

    def doLoadWithData(self, patientId):
        serializer = DatabaseDeserializer(self.wizard().getDatabase())

        name, blob = serializer.getAudioFile(patientId, 1)
        self.audio1.setName(name)
        self.audio1._blob = blob

        name, blob = serializer.getAudioFile(patientId, 2)
        self.audio2.setName(name)
        self.audio2._blob = blob

        name, blob = serializer.getAudioFile(patientId, 3)
        self.audio3.setName(name)
        self.audio3._blob = blob

        name, blob = serializer.getAudioFile(patientId, 4)
        self.audio4.setName(name)
        self.audio4._blob = blob

        name, blob = serializer.getAudioFile(patientId, 5)
        self.audio5.setName(name)
        self.audio5._blob = blob

        name, blob = serializer.getAudioFile(patientId, 6)
        self.audio6.setName(name)
        self.audio6._blob = blob

        name, blob = serializer.getAudioFile(patientId, 7)
        self.audio7.setName(name)
        self.audio7._blob = blob

        name, blob = serializer.getAudioFile(patientId, 8)
        self.audio8.setName(name)
        self.audio8._blob = blob
