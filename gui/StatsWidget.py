from PyQt5.QtWidgets import QTabWidget, QVBoxLayout, QLabel, QWidget
from PyQt5.QtGui import QFont
from Statistics.Stats import Stats
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Qt5Agg')


class PlotWidget(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(PlotWidget, self).__init__(fig)
        self.setParent(parent)


class StatsWidget(QTabWidget):
    def __init__(self, stats: Stats, icon):
        super(StatsWidget, self).__init__()
        self.stats = stats
        self.setWindowTitle("Database statistics")
        self.setWindowIcon(icon)

        # RDC diagnosis histograms
        self.plotWidgetAxis11 = PlotWidget(self)
        self.plotWidgetAxis12Right = PlotWidget(self)
        self.plotWidgetAxis12Left = PlotWidget(self)
        self.plotWidgetAxis13Right = PlotWidget(self)
        self.plotWidgetAxis13Left = PlotWidget(self)
        self.plotWidgetAxis21 = PlotWidget(self)

        # general statistics data
        self.meanAgeLabel = QLabel()
        self.meanAgeLabel.setFont(QFont("Arial", 10, QFont.Bold))
        self.sexHistogram = PlotWidget(self)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.addWidget(self.sexHistogram)
        self.verticalLayout.addWidget(self.meanAgeLabel)
        self.genericStatisticsWidget = QWidget()
        self.genericStatisticsWidget.setLayout(self.verticalLayout)

        # load with current values
        self.update()

        self.addTab(self.plotWidgetAxis11, "Axis11 Histogram")
        self.addTab(self.plotWidgetAxis12Right, "Axis12 Right Histogram")
        self.addTab(self.plotWidgetAxis12Left, "Axis12 Left Histogram")
        self.addTab(self.plotWidgetAxis13Right, "Axis13 Right Histogram")
        self.addTab(self.plotWidgetAxis13Left, "Axis13 Left Histogram")
        self.addTab(self.plotWidgetAxis21, "Axis2 Chronic Pain Histogram")
        self.addTab(self.genericStatisticsWidget, "General statistics")

    def _updateDiagnosisHistograms(self):
        labels, counts = self.stats.getAxis11Histogram()
        self.plotWidgetAxis11.axes.clear()
        self.plotWidgetAxis11.axes.bar(labels, counts, align='center')
        self.plotWidgetAxis11.draw()

        labels, counts = self.stats.getAxis12RightHistogram()
        self.plotWidgetAxis12Right.axes.clear()
        self.plotWidgetAxis12Right.axes.bar(labels, counts, align='center')
        self.plotWidgetAxis12Right.draw()

        labels, counts = self.stats.getAxis12LeftHistogram()
        self.plotWidgetAxis12Left.axes.clear()
        self.plotWidgetAxis12Left.axes.bar(labels, counts, align='center')
        self.plotWidgetAxis12Left.draw()

        labels, counts = self.stats.getAxis13RightHistogram()
        self.plotWidgetAxis13Right.axes.clear()
        self.plotWidgetAxis13Right.axes.bar(labels, counts, align='center')
        self.plotWidgetAxis13Right.draw()

        labels, counts = self.stats.getAxis13LeftHistogram()
        self.plotWidgetAxis13Left.axes.clear()
        self.plotWidgetAxis13Left.axes.bar(labels, counts, align='center')
        self.plotWidgetAxis13Left.draw()

        labels, counts = self.stats.getAxis21Histogram()
        self.plotWidgetAxis21.axes.clear()
        self.plotWidgetAxis21.axes.bar(labels, counts, align='center')
        self.plotWidgetAxis21.draw()

    def _updateGeneralStats(self):
        labels, counts = self.stats.getGenderDistribution()
        self.sexHistogram.axes.cla()
        self.sexHistogram.axes.bar(labels, counts, align='center')
        self.sexHistogram.draw()
        self.meanAgeLabel.setText(": ".join(["Mean patient age", str(self.stats.getMeanAge())]))

    def update(self):
        self._updateDiagnosisHistograms()
        self._updateGeneralStats()
