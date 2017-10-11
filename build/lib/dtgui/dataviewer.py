# -*- coding: utf-8 -*-

import numpy as np
from pyqtgraph import QtGui, QtCore
import pyqtgraph as pg

class DataViewer(QtGui.QWidget):
    """ Widget displaying raw and baseline-removed data """
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.plot_widget = pg.PlotWidget(title = 'Spectral data', 
                                         labels = {'left': 'Intensity (counts)', 
                                                   'bottom': 'Wavenumber'})

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
    def plot_raw_data(self, wavenumber, counts):
        """
        Plot a raw spectra.

        Parameters
        ----------
        wavenumber : ndarray
            Wavenumber of the measurement
        counts : ndarray
            Spectral data
        """
        self.raw_data_item.setData(x = np.array(wavenumber), y = np.array(counts))
    
    @QtCore.pyqtSlot()
    def clear_raw_data(self):
        """ Clear raw data from plot """
        self.raw_data_item.clear()
    
    @QtCore.pyqtSlot(object, object)
    def plot_baseline(self, wavenumber, baseline):
        """
        Plot a raw spectra.

        Parameters
        ----------
        wavenumber : ndarray
            Wavenumber of the measurement
        baseline : ndarray
            Baseline of spectral data
        """
        self.baseline_data_item.setData(x = np.array(wavenumber), y = np.array(baseline))

    @QtCore.pyqtSlot()
    def clear_baseline_data(self):
        """ Clear baseline from plot """
        self.baseline_data_item.clear()