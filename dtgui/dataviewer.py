# -*- coding: utf-8 -*-

import numpy as np
from pyqtgraph import QtGui, QtCore
import pyqtgraph as pg

class DataViewer(QtGui.QWidget):
    """ Widget displaying raw and baseline-removed data """
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.plot_widget = pg.PlotWidget(title = 'Data', 
                                         labels = {'left': 'Counts', 
                                                   'bottom': 'Abscissa'})

        self.raw_data_item = pg.PlotDataItem(symbol = 'o', symbolBrush = pg.mkBrush('g'), 
                                             symbolPen = None, pen = None, symbolSize = 3)
        self.baseline_data_item = pg.PlotDataItem(symbol = 'o', symbolBrush = pg.mkBrush('r'), 
                                                  symbolPen = None, pen = None, symbolSize = 3)
        
        self.plot_widget.addItem(self.raw_data_item)
        self.plot_widget.addItem(self.baseline_data_item)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.plot_widget)

        self.setLayout(layout)
    
    @QtCore.pyqtSlot(object, object)
    def plot_raw_data(self, x, y):
        """
        Plot a raw data.

        Parameters
        ----------
        x, y : ndarray
        """
        self.raw_data_item.setData(x = np.array(x), y = np.array(y))
    
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
        self.baseline_data_item.setData(x = np.array(x), y = np.array(y))

    @QtCore.pyqtSlot()
    def clear_baseline_data(self):
        """ Clear baseline from plot """
        self.baseline_data_item.clear()