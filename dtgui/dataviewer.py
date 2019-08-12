# -*- coding: utf-8 -*-

import numpy as np
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg


class DataViewer(QtWidgets.QWidget):
    """ Widget displaying raw and baseline-removed data """

    error_message_signal = QtCore.pyqtSignal(str)
    trim_bounds_signal = QtCore.pyqtSignal(float, float)
    background_markers_signal = QtCore.pyqtSignal(list)

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.plot_widget = pg.PlotWidget(
            title="<font color = 'green'>Raw data</font>, <font color='red'>Baseline</font>",
            labels={"left": "Ordinate", "bottom": "Abscissa"},
        )

        self.raw_data_item = pg.PlotDataItem(
            symbol="o",
            symbolBrush=pg.mkBrush("g"),
            symbolPen=None,
            pen=None,
            symbolSize=3,
            name="Raw data",
        )
        self.baseline_data_item = pg.PlotDataItem(
            symbol="o",
            symbolBrush=pg.mkBrush("r"),
            symbolPen=None,
            pen=None,
            symbolSize=3,
            name="Baseline",
        )
        self.data_bounds_region = pg.LinearRegionItem()
        self.data_bounds_region.hide()

        # Background markers are pyqtgraph InfiniteLines that
        # indicate points where background is expected
        self.background_markers = list()

        self.plot_widget.addItem(self.raw_data_item)
        self.plot_widget.addItem(self.baseline_data_item)
        self.plot_widget.addItem(self.data_bounds_region)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.plot_widget)

        self.setLayout(layout)

    @QtCore.pyqtSlot(bool)
    def toggle_trim_widget(self, toggle):
        if toggle:
            self.data_bounds_region.setBounds(self.raw_data_item.dataBounds(ax=0))
            self.data_bounds_region.show()
        else:
            self.data_bounds_region.hide()

    @QtCore.pyqtSlot()
    def add_background_marker(self):
        new_marker = pg.InfiniteLine(pos=0, angle=90, movable=True)
        new_marker.sigPositionChanged.connect(self.actualize_bg_markers)
        self.plot_widget.addItem(new_marker)
        self.background_markers.append(new_marker)

    @QtCore.pyqtSlot()
    def clear_background_markers(self):
        for item in self.background_markers:
            self.plot_widget.getPlotItem().removeItem(item)
        self.background_markers.clear()
        self.background_markers_signal.emit(list())

    @QtCore.pyqtSlot(object)
    def actualize_bg_markers(self, *args):
        self.background_markers_signal.emit(
            [marker.value() for marker in self.background_markers]
        )

    @QtCore.pyqtSlot()
    def trim_bounds(self):
        # getRegion() return a 2-tuple of data bounds, not indices
        self.trim_bounds_signal.emit(*self.data_bounds_region.getRegion())

    @QtCore.pyqtSlot(object, object)
    def plot_raw_data(self, x, y):
        """
        Plot a raw data.

        Parameters
        ----------
        x, y : ndarray
        """
        self.raw_data_item.setData(x=np.array(x), y=np.array(y))

    @QtCore.pyqtSlot()
    def clear_raw_data(self):
        """ Clear raw data from plot """
        self.raw_data_item.clear()

    @QtCore.pyqtSlot(object, object)
    def plot_baseline(self, x, y):
        """
        Plot baseline.

        Parameters
        ----------
        x : ndarray
            x of the measurement
        baseline : ndarray
            Baseline of spectral data
        """
        self.baseline_data_item.setData(x=np.array(x), y=np.array(y))

    @QtCore.pyqtSlot()
    def clear_baseline_data(self):
        """ Clear baseline from plot """
        self.baseline_data_item.clear()
