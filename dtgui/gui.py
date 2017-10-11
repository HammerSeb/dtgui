# -*- coding: utf-8 -*-

import sys

import pyqtgraph as pg
from pyqtgraph import QtCore, QtGui
from qdarkstyle import load_stylesheet_pyqt5

from .batch import BatchProcessDialog
from .control_bar import ControlBar
from .controller import Controller
from .dataviewer import DataViewer
from .error_aware import ErrorAware


class DtGui(QtGui.QMainWindow, metaclass = ErrorAware):

    raw_data_path = QtCore.pyqtSignal(str)
    export_data_path = QtCore.pyqtSignal(str)
    error_message_signal = QtCore.pyqtSignal(str)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.controller = Controller(parent = self) # TODO: different thread?

        self.controls = ControlBar(parent = self)
        self.raw_data_path.connect(self.controller.load_raw_data)
        self.controller.raw_data_loaded_signal.connect(self.controls.toggle_baseline_controls)
        self.export_data_path.connect(self.controller.export_data)
        self.controls.baseline_parameters_signal.connect(self.controller.compute_baseline)

        self.data_viewer = DataViewer(parent = self)
        self.controller.raw_plot_signal.connect(self.data_viewer.plot_raw_data)
        self.controller.baseline_plot_signal.connect(self.data_viewer.plot_baseline)
        self.controller.clear_raw_signal.connect(self.data_viewer.clear_raw_data)
        self.controller.clear_baseline_signal.connect(self.data_viewer.clear_baseline_data)
        self.data_viewer.trim_bounds_signal.connect(self.controller.trim_data_bounds)
        
        # Data trimming
        self.controls.show_trim_widget.connect(self.data_viewer.toggle_trim_widget)
        self.controls.trim_bounds_signal.connect(self.data_viewer.trim_bounds)

        self.menu_bar = self.menuBar()

        load_data_action = QtGui.QAction('Load data (.csv)', self)
        load_data_action.triggered.connect(self.load_raw_data)
        self.menu_bar.addAction(load_data_action)

        export_bs_data_action = QtGui.QAction('Export corrected data (.csv)', self)
        export_bs_data_action.triggered.connect(self.export_bs_data)
        self.controller.raw_data_loaded_signal.connect(export_bs_data_action.setEnabled)
        self.menu_bar.addAction(export_bs_data_action)
        export_bs_data_action.setEnabled(False)

        batch_process_action = QtGui.QAction('Batch process', self)
        batch_process_action.triggered.connect(self.launch_batch_process)
        self.controller.raw_data_loaded_signal.connect(batch_process_action.setEnabled)
        self.menu_bar.addSeparator()
        self.menu_bar.addAction(batch_process_action)
        batch_process_action.setEnabled(False)

        self.error_message_signal.connect(self.show_error_message)
        self.controller.error_message_signal.connect(self.show_error_message)
        self.data_viewer.error_message_signal.connect(self.show_error_message)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.data_viewer)
        layout.addWidget(self.controls)

        self.central_widget = QtGui.QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

        self.setWindowTitle('DTGUI - Baseline-removal via DTCWT')
        self.setGeometry(0, 0, 1000, 400)
        self.center_window()
        self.show()

    @QtCore.pyqtSlot()
    def load_raw_data(self):
        fname = QtGui.QFileDialog.getOpenFileName(parent = self, caption = 'Load data', filter = '*.csv')[0]
        if fname:
            self.raw_data_path.emit(fname)
    
    @QtCore.pyqtSlot()
    def export_bs_data(self):
        fname = QtGui.QFileDialog.getSaveFileName(parent = self, caption = 'Export data', filter = '*.csv')[0]
        if fname:
            self.export_data_path.emit(fname)
    
    @QtCore.pyqtSlot()
    def launch_batch_process(self):
        self.dialog = BatchProcessDialog(self.controls.baseline_parameters(), parent = self)
        self.dialog.exec_()

    @QtCore.pyqtSlot()
    def center_window(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    @QtCore.pyqtSlot(str)
    def show_error_message(self, msg):
        self.error_dialog = QtGui.QErrorMessage(parent = self)
        self.error_dialog.showMessage(msg)


def run():
    app = QtGui.QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet_pyqt5())
    gui = DtGui()
    sys.exit(app.exec_())
