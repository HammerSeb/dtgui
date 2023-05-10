# -*- coding: utf-8 -*-

import sys

import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
from qdarkstyle import load_stylesheet_pyqt5

from .batch import BatchProcessDialog
from .control_bar import ControlBar
from .controller import Controller
from .dataviewer import DataViewer
from .error_aware import ErrorAware


class DtGui(QtWidgets.QMainWindow, metaclass=ErrorAware):

    raw_data_path = QtCore.pyqtSignal(str)
    export_data_path = QtCore.pyqtSignal(str)

    error_message_signal = QtCore.pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.controller = Controller()
        self._control_thread = QtCore.QThread()
        self.controller.moveToThread(self._control_thread)
        self._control_thread.start()

        self.raw_data_path.connect(self.controller.load_raw_data)
        self.export_data_path.connect(self.controller.export_data)

        self.controls = ControlBar(parent=self)
        self.controls.setEnabled(False)
        self.controller.raw_data_loaded_signal.connect(self.controls.setEnabled)
        self.controls.baseline_parameters_signal.connect(
            self.controller.compute_baseline
        )

        self.data_viewer = DataViewer(parent=self)
        self.controller.raw_plot_signal.connect(self.data_viewer.plot_raw_data)
        self.controller.baseline_plot_signal.connect(self.data_viewer.plot_baseline)
        self.controller.clear_raw_signal.connect(self.data_viewer.clear_raw_data)
        self.controller.clear_baseline_signal.connect(
            self.data_viewer.clear_baseline_data
        )
        self.data_viewer.trim_bounds_signal.connect(self.controller.trim_data_bounds)
        self.controls.add_background_marker_signal.connect(
            self.data_viewer.add_background_marker
        )
        self.controls.clear_background_markers_signal.connect(
            self.data_viewer.clear_background_markers
        )
        self.data_viewer.background_markers_signal.connect(
            self.controller.update_background_markers
        )

        self.controls.show_trim_widget.connect(self.data_viewer.toggle_trim_widget)
        self.controls.trim_bounds_signal.connect(self.data_viewer.trim_bounds)

        self.error_message_signal.connect(self.show_error_message)
        self.controller.error_message_signal.connect(self.show_error_message)
        self.data_viewer.error_message_signal.connect(self.show_error_message)

        load_raw_data_action = QtWidgets.QAction("Load CSV data", self)
        load_raw_data_action.triggered.connect(self.load_raw_data)

        export_bs_data_action = QtWidgets.QAction(
            "Export background-subtracted data", self
        )
        export_bs_data_action.triggered.connect(self.export_bs_data)
        export_bs_data_action.setEnabled(False)
        self.controller.raw_data_loaded_signal.connect(export_bs_data_action.setEnabled)

        launch_batch_process_action = QtWidgets.QAction("Launch batch process", self)
        launch_batch_process_action.triggered.connect(self.launch_batch_process)

        menu_bar = self.menuBar()
        menu_bar.addAction(load_raw_data_action)
        menu_bar.addAction(export_bs_data_action)
        menu_bar.addAction(launch_batch_process_action)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.data_viewer)
        layout.addWidget(self.controls)

        self.central_widget = QtWidgets.QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

        self.setWindowTitle("DTGUI - Baseline-removal via DTCWT")
        self.center_window()
        self.show()

    def closeEvent(self, event):
        self._control_thread.quit()
        self._control_thread.wait()
        super().closeEvent(event)

    @QtCore.pyqtSlot()
    def center_window(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    @QtCore.pyqtSlot()
    def load_raw_data(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(
            parent=self, caption="Load data", filter="*.csv"
        )[0]
        if fname:
            self.raw_data_path.emit(fname)

    @QtCore.pyqtSlot()
    def export_bs_data(self):
        fname = QtWidgets.QFileDialog.getSaveFileName(
            parent=self, caption="Export data", filter="*.csv"
        )[0]
        if fname:
            self.export_data_path.emit(fname)

    @QtCore.pyqtSlot()
    def launch_batch_process(self):
        self.dialog = BatchProcessDialog(
            self.controls.baseline_parameters(), parent=self
        )
        return self.dialog.exec_()

    @QtCore.pyqtSlot(str)
    def show_error_message(self, msg):
        self.error_dialog = QtWidgets.QErrorMessage(parent=self)
        self.error_dialog.showMessage(msg)


def run():

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet_pyqt5())
    gui = DtGui()
    sys.exit(app.exec_())
