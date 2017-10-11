# -*- coding: utf-8 -*-

from pyqtgraph import QtCore, QtGui
from pywt import Modes

from .batch import BatchProcessDialog

from skued.baseline import ALL_COMPLEX_WAV, ALL_FIRST_STAGE

class ControlBar(QtGui.QWidget):

    baseline_parameters_signal = QtCore.pyqtSignal(dict)
    raw_data_path = QtCore.pyqtSignal(str)
    export_data_path = QtCore.pyqtSignal(str)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.load_spectra_btn = QtGui.QPushButton('Load spectra (.csv)')
        self.load_spectra_btn.clicked.connect(self.load_raw_data)

        self.export_spectra_btn = QtGui.QPushButton('Export corrected spectra')
        self.export_spectra_btn.clicked.connect(self.export_bs_data)

        btns = QtGui.QHBoxLayout()
        btns.addWidget(self.load_spectra_btn)
        btns.addWidget(self.export_spectra_btn)

        file_controls = QtGui.QGroupBox(title = 'File and batches', parent = self)
        file_controls.setLayout(btns)

        self.first_stage_cb = QtGui.QComboBox()
        self.first_stage_cb.addItems(ALL_FIRST_STAGE)
        if 'sym6' in ALL_FIRST_STAGE:
            self.first_stage_cb.setCurrentText('sym6')

        self.wavelet_cb = QtGui.QComboBox()
        self.wavelet_cb.addItems(ALL_COMPLEX_WAV)
        if 'qshift3' in ALL_COMPLEX_WAV:
            self.wavelet_cb.setCurrentText('qshift3')

        self.mode_cb = QtGui.QComboBox()
        self.mode_cb.addItems(Modes.modes)
        if 'smooth' in Modes.modes:
            self.mode_cb.setCurrentText('constant')
        
        self.max_iter_widget = QtGui.QSpinBox()
        self.max_iter_widget.setRange(0, 1000)
        self.max_iter_widget.setValue(100)

        self.level_widget = QtGui.QSpinBox()
        self.level_widget.setMinimum(0)
        self.level_widget.setValue(1)

        self.compute_baseline_btn = QtGui.QPushButton('Compute baseline', parent = self)
        self.compute_baseline_btn.clicked.connect(lambda _: self.baseline_parameters_signal.emit(self.baseline_parameters()))

        self.baseline_controls = QtGui.QFormLayout()
        self.baseline_controls.addRow('First stage wavelet: ', self.first_stage_cb)
        self.baseline_controls.addRow('Dual-tree wavelet: ', self.wavelet_cb)
        self.baseline_controls.addRow('Extensions mode: ', self.mode_cb)
        self.baseline_controls.addRow('Iterations: ', self.max_iter_widget)
        self.baseline_controls.addRow('Decomposition level: ', self.level_widget)
        self.baseline_controls.addRow(self.compute_baseline_btn)

        self.baseline_computation = QtGui.QGroupBox(title = 'Baseline parameters', parent = self)
        self.baseline_computation.setLayout(self.baseline_controls)

        self.process_batch_btn = QtGui.QPushButton('Batch process')
        self.process_batch_btn.clicked.connect(self.launch_batch_process)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(file_controls)
        layout.addWidget(self.baseline_computation)
        layout.addWidget(self.process_batch_btn)

        self.setLayout(layout)
        self.resize(self.minimumSize())
        self.toggle_baseline_controls(False)

    def load_raw_data(self):
        fname = QtGui.QFileDialog.getOpenFileName(parent = self, caption = 'Load spectra', filter = '*.csv')[0]
        if fname:
            self.raw_data_path.emit(fname)
    
    def export_bs_data(self):
        fname = QtGui.QFileDialog.getSaveFileName(parent = self, caption = 'Export spectra', filter = '*.csv')[0]
        if fname:
            self.export_data_path.emit(fname)
    
    def launch_batch_process(self):
        self.dialog = BatchProcessDialog(self.baseline_parameters(), parent = self)
        self.dialog.exec_()
    
    @QtCore.pyqtSlot(bool)
    def toggle_baseline_controls(self, toggle):
        """ Toggle on or off the baseline computation controls """
        self.baseline_computation.setEnabled(toggle)
        self.process_batch_btn.setEnabled(toggle)
        self.export_spectra_btn.setEnabled(toggle)

    def baseline_parameters(self):
        """ Returns a dictionary of baseline-computation parameters """
        return {'first_stage': self.first_stage_cb.currentText(),
                'wavelet': self.wavelet_cb.currentText(),
                'mode': self.mode_cb.currentText(),
                'max_iter': self.max_iter_widget.value(),
                'level': self.level_widget.value()}