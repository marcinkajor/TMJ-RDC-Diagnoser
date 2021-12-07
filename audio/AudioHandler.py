from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont
import numpy as np
from scipy.io import wavfile
import winsound
import io
import multiprocessing as multiprocess
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor, Button
import numpy as np
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

    def serialize(self, filePath: str, fs, data):
        try:
            wavfile.write(filePath, fs, data)
        except Exception as e:
            self.writeErrorNotification(e)


class PlotWidget(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(PlotWidget, self).__init__(self.fig)
        self.setParent(parent)

# AudioManager class uses the winsound module which is Windows specific and makes the code not portable
# the problem with platform independent audio modules is that they do not support 'weird' sampling rates
# like 4k which is the case of audio signals recorded with Littmann stethoscope
# To provide the non-blocking behaviour of the audio playback, the multiprocess module is used
# as it facilitates immediate termination of the underlying process (not so simple when using threading)
# The playAudio function must be global to be spawn in multiprocess.Process


def playAudio(audio):
    winsound.PlaySound(audio, winsound.SND_MEMORY)


class AudioManager(SaveFile, QtWidgets.QWidget):
    def __init__(self, filename: str, binaryData, serializer: AudioSerializer, icon):
        SaveFile.__init__(self, self, icon)
        QtWidgets.QWidget.__init__(self)
        self.saveButton = QtWidgets.QPushButton("Save audio file")
        self.playButton = QtWidgets.QPushButton("Play audio file")
        self.stopButton = QtWidgets.QPushButton("Stop playing")
        self.savePlotButton = QtWidgets.QPushButton("Save plot")
        self.segmentationButton = QtWidgets.QPushButton("Segmentation")
        self.saveButton.clicked.connect(self._onSaveButtonClicked)
        self.playButton.clicked.connect(self._onPlayButtonClicked)
        self.stopButton.clicked.connect(self._onStopPlayingButtonClicked)
        self.savePlotButton.clicked.connect(self._onSavePlotButtonClicked)
        self.segmentationButton.clicked.connect(self._onSegmentationButtonClicked)

        self.fileName = filename
        self.label = QtWidgets.QLabel("Audio name")
        font = QFont("Arial", 9)
        font.setBold(True)
        self.label.setFont(font)
        self.nameWidget = QtWidgets.QLineEdit()
        self.nameWidget.setText(self.fileName)
        self.nameWidget.setReadOnly(True)
        self.serializer = serializer

        self.binaryData = binaryData
        self.fs, self.signal = self.parseWavFile(binaryData)

        self.plot = PlotWidget(self)
        # TODO: the self._normalizeData() causes significant delay when generating plots
        self.plot.axes.plot(self._timeVector(self.fs, self.signal), self.signal)

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
        self.layout.addWidget(self.segmentationButton)
        self.setLayout(self.layout)

    def _onSaveButtonClicked(self):
        try:
            path, fileFilter = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', filter="Audio file (*.wav)")
            self.serializer.serialize(path, self.fs, self.signal)
        except Exception as e:
            print(e)

    def _onPlayButtonClicked(self):
        try:
            self.playbackProcess = multiprocess.Process(target=playAudio, args=(self.binaryData,))
            self.playbackProcess.start()
        except Exception as e:
            print(e)

    def _onSavePlotButtonClicked(self):
        dpi, ok = QtWidgets.QInputDialog.getInt(self, "Choose the dpi", "dpi", 100, 100, 1000)
        try:
            if ok:
                path, fileFilter = QtWidgets.QFileDialog.getSaveFileName(self, 'Save plot', filter="(*.png)")
                self.plot.fig.savefig(path, dpi=dpi)
            else:
                self.writeErrorNotification("Cannot write with no dpi specified")
        except Exception as e:
            self.writeErrorNotification(e)

    def _onStopPlayingButtonClicked(self):
        try:
            self.playbackProcess.terminate()
        except Exception as e:
            print(e)

    def _onKeyPressedEvent(self, event):
        if self.allowPicking:
            x = int(round(event.xdata))
            y = int(round(event.ydata))
            self.points.append((x, y))
            visiblePoint = self.ax.plot(x, y, 'rx')
            self.visiblePoints.append(visiblePoint[0])
            xleft, xright = self.ax.get_xlim()
            yleft, yright = self.ax.get_ylim()
            plt.draw()
            self.ax.set_xlim(xleft, xright)
            self.ax.set_ylim(yleft, yright)
            print(x, y)

    def _onStartButtonClicked(self, event):
        print("Start")
        self.allowPicking = True

    def _onStopButtonClicked(self, event):
        print("Stop")
        self.allowPicking = False

    def _onCancelButtonClicked(self, event):
        print("Cancel")
        if self.points:
            self.points.pop()
            self.visiblePoints.pop().remove()
            plt.draw()

    def _onClearAllButtonClicked(self, event):
        print("Clear all")
        self.points.clear()
        # TODO: this takes a lot of time
        while self.visiblePoints:
            self.visiblePoints.pop().remove()

    def _onSegmentationButtonClicked(self):
        self.fig, self.ax = plt.subplots()
        plt.plot(self.signal, zorder=1)
        self.cursor = Cursor(self.ax, useblit=True, color='red', linewidth=1)
        self.points = []
        self.visiblePoints = []
        self.allowPicking = False
        startButtonPos = plt.axes([0.12, 0.9, 0.1, 0.075])
        stopButtonPos = plt.axes([0.24, 0.9, 0.1, 0.075])
        cancelButtonPos = plt.axes([0.36, 0.9, 0.1, 0.075])
        clearAllButtonPos = plt.axes([0.48, 0.9, 0.1, 0.075])
        self.startButton = Button(startButtonPos, 'Start')
        self.stopButton = Button(stopButtonPos, 'Stop')
        self.cancelButton = Button(cancelButtonPos, 'Cancel')
        self.clearAllButton = Button(clearAllButtonPos, 'Clear all')
        self.startButton.on_clicked(self._onStartButtonClicked)
        self.stopButton.on_clicked(self._onStopButtonClicked)
        self.cancelButton.on_clicked(self._onCancelButtonClicked)
        self.clearAllButton.on_clicked(self._onClearAllButtonClicked)
        self.fig.canvas.mpl_connect('key_press_event', self._onKeyPressedEvent)
        plt.show()

    @staticmethod
    def parseWavFile(binaryData) -> tuple:
        fs, signal = wavfile.read(io.BytesIO(binaryData))
        # try:
        #     numberOfChannels = 2 if signal.shape[1] else 1
        # except Exception as e:
        #     str(e)
        #     numberOfChannels = 1
        return fs, signal

    @staticmethod
    def _timeVector(fs, signal):
        return [x * 1 / fs for x in range(len(signal))]

    @staticmethod
    def _normalizeData(signal, norm_type='minus_one_one'):
        sig_min = int(np.min(signal))
        sig_max = int(np.max(signal))
        max_min_diff = (sig_max - sig_min)
        if norm_type == 'zero_one':
            return [(signal[idx] - sig_min)/max_min_diff for idx in range(len(signal))]
        elif norm_type == 'minus_one_one':
            return [2*(signal[idx] - sig_min)/max_min_diff - 1 for idx in range(len(signal))]
