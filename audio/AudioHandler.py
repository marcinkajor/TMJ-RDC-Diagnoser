from PyQt5 import QtWidgets
import winsound  # Note that this is Windows specific module
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Qt5Agg')


class SaveFile:
    def __init__(self, parent, icon):
        self.parent = parent
        self.icon = icon

    def writeErrorNotification(self, text: str):
        message = QtWidgets.QMessageBox(self.parent)
        message.setWindowIcon(self.icon)
        message.setWindowTitle("Error")
        try:
            message.setText(str(text))
        except Exception as e:
            print(e)
        message.exec_()


class AudioSerializer(SaveFile):
    def __init__(self, parent, icon):
        super().__init__(parent, icon)
        self.parent = parent
        self.icon = icon

    def serialize(self, filePath: str, binaryData):
        try:
            with open(filePath, 'wb') as audioFile:
                audioFile.write(binaryData)
        except Exception as e:
            self.writeErrorNotification(e)


class PlotWidget(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(PlotWidget, self).__init__(self.fig)
        self.setParent(parent)


class AudioManager(SaveFile, QtWidgets.QWidget):
    def __init__(self, filename: str, binaryData, serializer: AudioSerializer, icon):
        SaveFile.__init__(self, self, icon)
        QtWidgets.QWidget.__init__(self)
        self.saveButton = QtWidgets.QPushButton("Save audio file")
        self.playButton = QtWidgets.QPushButton("Play audio file")
        self.stopButton = QtWidgets.QPushButton("Stop playing")
        self.savePlotButton = QtWidgets.QPushButton("Save plot")
        self.saveButton.clicked.connect(self._onSaveButtonClicked)
        self.playButton.clicked.connect(self._onPlayButtonClicked)
        self.stopButton.clicked.connect(self._onStopPlayingButtonClicked)
        self.savePlotButton.clicked.connect(self._onSavePlotButtonClicked)

        self.fileName = filename
        self.label = QtWidgets.QLabel("Audio name")
        self.nameWidget = QtWidgets.QLineEdit()
        self.nameWidget.setText(self.fileName)
        self.nameWidget.setReadOnly(True)
        self.binaryData = binaryData
        self.serializer = serializer

        self.plot = PlotWidget(self)
        self.plot.axes.plot(np.frombuffer(self.binaryData, dtype='int16'))
        self.plot.axes.set_xlabel("Time [s]")
        self.plot.axes.set_ylabel("Amplitude")
        self.plot.draw()

        self.layout = QtWidgets.QVBoxLayout()
        self.nameLayout = QtWidgets.QHBoxLayout()
        self.nameLayout.addWidget(self.label)
        self.nameLayout.addWidget(self.nameWidget)
        self.layout.addLayout(self.nameLayout)
        self.layout.addWidget(self.plot)
        self.layout.addWidget(self.saveButton)
        self.layout.addWidget(self.playButton)
        self.layout.addWidget(self.stopButton)
        self.layout.addWidget(self.savePlotButton)
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

    def _onSavePlotButtonClicked(self):
        dpi, ok = QtWidgets.QInputDialog.getInt(self, "Choose the dpi", "dpi", 100, 100, 1000)
        try:
            path, fileFilter = QtWidgets.QFileDialog.getSaveFileName(self, 'Save plot', filter="(*.png)")
            if ok:
                self.plot.fig.savefig(path, dpi=dpi)
            else:
                print("Plotting with default dpi=500")
                self.plot.fig.savefig(path, dpi=500)
        except Exception as e:
            self.writeErrorNotification(e)

    @staticmethod
    def _onStopPlayingButtonClicked():
        pass
