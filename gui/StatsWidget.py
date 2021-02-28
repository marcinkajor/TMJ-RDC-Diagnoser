from PyQt5.QtWidgets import QTabWidget, QSizePolicy
from Statistics.Stats import Stats
import numpy as np
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
        labels, counts = np.unique(self.stats.getAxis11Histogram(), return_counts=True)
        plotWidgetAxis11 = PlotWidget(self)

        plotWidgetAxis11.axes.bar(labels, counts, align='center')

        labels, counts = np.unique(self.stats.getAxis12RightHistogram(), return_counts=True)
        plotWidgetAxis12Right = PlotWidget(self)
        plotWidgetAxis12Right.axes.bar(labels, counts, align='center')

        labels, counts = np.unique(self.stats.getAxis12LeftHistogram(), return_counts=True)
        plotWidgetAxis12Left = PlotWidget(self)
        plotWidgetAxis12Left.axes.bar(labels, counts, align='center')

        labels, counts = np.unique(self.stats.getAxis13RightHistogram(), return_counts=True)
        plotWidgetAxis13Right = PlotWidget(self)
        plotWidgetAxis13Right.axes.bar(labels, counts, align='center')

        labels, counts = np.unique(self.stats.getAxis13LeftHistogram(), return_counts=True)
        plotWidgetAxis13Left = PlotWidget(self)
        plotWidgetAxis13Left.axes.bar(labels, counts, align='center')

        self.addTab(plotWidgetAxis11, "Axis11 Histogram")
        self.addTab(plotWidgetAxis12Right, "Axis12 Right Histogram")
        self.addTab(plotWidgetAxis12Left, "Axis12 Left Histogram")
        self.addTab(plotWidgetAxis13Right, "Axis13 Right Histogram")
        self.addTab(plotWidgetAxis13Left, "Axis13 Left Histogram")
