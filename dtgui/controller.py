# -*- coding: utf-8 -*-

import numpy as np
from pyqtgraph import QtCore
from skued import baseline_dt

class Controller(QtCore.QObject):

    raw_plot_signal = QtCore.pyqtSignal(object, object)
    baseline_plot_signal = QtCore.pyqtSignal(object, object)

    clear_raw_signal = QtCore.pyqtSignal()
    clear_baseline_signal = QtCore.pyqtSignal()

    raw_data_loaded_signal = QtCore.pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.abscissa = None
        self.raw_ordinates = None
        self.baseline = None

        self.clear_raw_signal.emit()
        self.clear_baseline_signal.emit()
        self.raw_data_loaded_signal.emit(False)
    
    @QtCore.pyqtSlot(str)
    def load_raw_data(self, fname):
        """ Read a CSV file. It is assumed that the CSV file has two columns (x, y)
        with no headers or footers. """
        self.abscissa, self.raw_ordinates = np.loadtxt(fname, delimiter = ',', unpack = True)
        self.raw_data_loaded_signal.emit(True)
        self.clear_raw_signal.emit()

        self.baseline = None
        self.clear_baseline_signal.emit()

        self.raw_plot_signal.emit(self.abscissa, self.raw_ordinates)
    
    @QtCore.pyqtSlot(str)
    def export_data(self, fname):
        if self.baseline is None:
            self.baseline = np.zeros_like(self.raw_ordinates)

        arr = np.empty(shape = (self.raw_ordinates.size, 2))
        arr[:,0] = self.abscissa
        arr[:,1] = self.raw_ordinates - self.baseline
        
        np.savetxt(fname, arr, delimiter = ',')

    @QtCore.pyqtSlot(dict)
    def compute_baseline(self, params):
        """ Compute dual-tree complex wavelet baseline. All parameters are
        passed to scikit-ued's baseline_dt function. """

        self.baseline = baseline_dt(self.raw_ordinates, **params)
        self.baseline_plot_signal.emit(self.abscissa, self.baseline)