# -*- coding: utf-8 -*-

from pyqtgraph import QtCore, QtGui
from pywt import Modes

from skued.baseline import ALL_COMPLEX_WAV, ALL_FIRST_STAGE

from .error_aware import ErrorAware

class ControlBar(QtGui.QWidget, metaclass = ErrorAware):

    baseline_parameters_signal = QtCore.pyqtSignal(dict)
    show_trim_widget = QtCore.pyqtSignal(bool)
    trim_bounds_signal = QtCore.pyqtSignal()


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        show_trim_bounds_btn = QtGui.QPushButton('Trim data bounds')
        show_trim_bounds_btn.setCheckable(True)
        show_trim_bounds_btn.toggled.connect(self.show_trim_widget)

        trigger_trim_btn = QtGui.QPushButton('Use current bounds')
        trigger_trim_btn.clicked.connect(self.trim_bounds_signal)
        trigger_trim_btn.clicked.connect(lambda: show_trim_bounds_btn.setChecked(False))
        show_trim_bounds_btn.toggled.connect(trigger_trim_btn.setEnabled)
        trigger_trim_btn.setEnabled(False)

        data_controls_layout = QtGui.QHBoxLayout()
        data_controls_layout.addWidget(show_trim_bounds_btn)
        data_controls_layout.addWidget(trigger_trim_btn)

        data_controls = QtGui.QGroupBox(title = 'Data massaging', parent = self)
        data_controls.setLayout(data_controls_layout)

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

        layout = QtGui.QVBoxLayout()
        layout.addWidget(data_controls)
        layout.addWidget(self.baseline_computation)
        layout.addStretch(1)

        self.setLayout(layout)
        self.resize(self.minimumSize())
        self.toggle_baseline_controls(False)
    
    @QtCore.pyqtSlot(bool)
    def toggle_baseline_controls(self, toggle):
        """ Toggle on or off the baseline computation controls """
        self.baseline_computation.setEnabled(toggle)

    def baseline_parameters(self):
        """ Returns a dictionary of baseline-computation parameters """
        return {'first_stage': self.first_stage_cb.currentText(),
                'wavelet': self.wavelet_cb.currentText(),
                'mode': self.mode_cb.currentText(),
                'max_iter': self.max_iter_widget.value(),
                'level': self.level_widget.value()}
