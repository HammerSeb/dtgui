# -*- coding: utf-8 -*-

import sys

import pyqtgraph as pg
from pyqtgraph import QtCore, QtGui
from qdarkstyle import load_stylesheet_pyqt5

from .controller import Controller
from .control_bar import ControlBar
from .dataviewer import DataViewer

class DtGui(QtGui.QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.controller = Controller(parent = self) # TODO: different thread?

        self.controls = ControlBar(parent = self)
        self.controls.raw_data_path.connect(self.controller.load_raw_data)
        self.controller.raw_data_loaded_signal.connect(self.controls.toggle_baseline_controls)
        self.controls.export_data_path.connect(self.controller.export_data)
        self.controls.baseline_parameters_signal.connect(self.controller.compute_baseline)

        self.data_viewer = DataViewer(parent = self)
        self.controller.raw_plot_signal.connect(self.data_viewer.plot_raw_data)
        self.controller.baseline_plot_signal.connect(self.data_viewer.plot_baseline)
        self.controller.clear_raw_signal.connect(self.data_viewer.clear_raw_data)
        self.controller.clear_baseline_signal.connect(self.data_viewer.clear_baseline_data)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.data_viewer)
        layout.addWidget(self.controls)

        self.central_widget = QtGui.QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

        self.setWindowTitle('SERS baseline-subtraction')
        self.setGeometry(0, 0, 1000, 400)
        self.center_window()
        self.show()

    @QtCore.pyqtSlot()
    def center_window(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

def run():
    app = QtGui.QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet_pyqt5())
    gui = DtGui()
    sys.exit(app.exec_())