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
        labels, counts = self.stats.getAxis11Histogram()
        plotWidgetAxis11 = PlotWidget(self)
        plotWidgetAxis11.axes.bar(labels, counts, align='center')

        labels, counts = self.stats.getAxis12RightHistogram()
        plotWidgetAxis12Right = PlotWidget(self)
        plotWidgetAxis12Right.axes.bar(labels, counts, align='center')

        labels, counts = self.stats.getAxis12LeftHistogram()
        plotWidgetAxis12Left = PlotWidget(self)
        plotWidgetAxis12Left.axes.bar(labels, counts, align='center')

        labels, counts = self.stats.getAxis13RightHistogram()
        plotWidgetAxis13Right = PlotWidget(self)
        plotWidgetAxis13Right.axes.bar(labels, counts, align='center')

        labels, counts = self.stats.getAxis13LeftHistogram()
        plotWidgetAxis13Left = PlotWidget(self)
        plotWidgetAxis13Left.axes.bar(labels, counts, align='center')

        # general statistics data
        meanAgeLabel = QLabel(": ".join(["Mean patient age", str(self.stats.getMeanAge())]))
        meanAgeLabel.setFont(QFont("Arial", 10, QFont.Bold))
        labels, counts = self.stats.getGenderDistribution()
        sexHistogram = PlotWidget(self)
        sexHistogram.axes.bar(labels, counts, align='center')
        verticalLayout = QVBoxLayout()
        verticalLayout.addWidget(sexHistogram)
        verticalLayout.addWidget(meanAgeLabel)
        genericStatisticsWidget = QWidget()
        genericStatisticsWidget.setLayout(verticalLayout)

        self.addTab(plotWidgetAxis11, "Axis11 Histogram")
        self.addTab(plotWidgetAxis12Right, "Axis12 Right Histogram")
        self.addTab(plotWidgetAxis12Left, "Axis12 Left Histogram")
        self.addTab(plotWidgetAxis13Right, "Axis13 Right Histogram")
        self.addTab(plotWidgetAxis13Left, "Axis13 Left Histogram")
        self.addTab(genericStatisticsWidget, "General statistics")
