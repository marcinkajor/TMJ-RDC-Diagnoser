from PyQt5 import QtWidgets
import winsound  # Note that this is Windows specific module


class AudioSerializer:
    def __init__(self, parent, icon):
        self.parent = parent
        self.icon = icon

    def serialize(self, filePath: str, binaryData):
        try:
            with open(filePath, 'wb') as audioFile:
                audioFile.write(binaryData)
        except Exception as e:
            self.writeErrorNotification(e)

    def writeErrorNotification(self, text: str):
        message = QtWidgets.QMessageBox(self.parent)
        message.setWindowIcon(self.icon)
        message.setWindowTitle("Error")
        try:
            message.setText(str(text))
        except Exception as e:
            print(e)
        message.exec_()


class AudioManager(QtWidgets.QWidget):
    def __init__(self, filename: str, binaryData, serializer: AudioSerializer):
        super().__init__()
        self.saveButton = QtWidgets.QPushButton("Save audio file")
        self.playButton = QtWidgets.QPushButton("Play audio file")
        self.stopButton = QtWidgets.QPushButton("Stop playing")
        self.saveButton.clicked.connect(self._onSaveButtonClicked)
        self.playButton.clicked.connect(self._onPlayButtonClicked)
        self.stopButton.clicked.connect(self._onStopPlayingButtonClicked)
        self.fileName = filename
        self.label = QtWidgets.QLabel("Audio name")
        self.nameWidget = QtWidgets.QLineEdit()
        self.nameWidget.setText(self.fileName)
        self.nameWidget.setReadOnly(True)
        self.binaryData = binaryData
        self.serializer = serializer
        self.layout = QtWidgets.QVBoxLayout()
        self.nameLayout = QtWidgets.QHBoxLayout()
        self.nameLayout.addWidget(self.label)
        self.nameLayout.addWidget(self.nameWidget)
        self.layout.addWidget(self.saveButton)
        self.layout.addWidget(self.playButton)
        self.layout.addWidget(self.stopButton)
        self.layout.addLayout(self.nameLayout)
        self.setLayout(self.layout)

    def _onSaveButtonClicked(self):
        try:
            path, fileFilter = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', filter="Audio file (*.wav)")
            self.serializer.serialize(path, self.binaryData)
        except Exception as e:
            print(e)

    def _onPlayButtonClicked(self):
        winsound.PlaySound(self.binaryData, winsound.SND_MEMORY)
        # TODO: replace with pyaudio to allow asynchronous playback

    @staticmethod
    def _onStopPlayingButtonClicked():
        pass
