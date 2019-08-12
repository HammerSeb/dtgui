# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets
from pywt import Modes

from skued.baseline import ALL_COMPLEX_WAV, ALL_FIRST_STAGE

from .error_aware import ErrorAware

EXPLANATION = """
The data fed to dtgui should be comma-separated values files (.csv). 
The first column is expected to be the abscissa values, 
while the second column should be the ordinates.
""".replace(
    "\n", ""
)

TRIM_TEXT = "Data can be trimmed. Drag the edges of the overlay. Data outside the bound will be removed."

BACKGROUND_MARKER_TEXT = """
Position background markers where you know the signal should only be composed of background.
""".replace(
    "\n", ""
)


class ControlBar(QtWidgets.QWidget, metaclass=ErrorAware):

    baseline_parameters_signal = QtCore.pyqtSignal(dict)
    show_trim_widget = QtCore.pyqtSignal(bool)
    trim_bounds_signal = QtCore.pyqtSignal()

    add_background_marker_signal = QtCore.pyqtSignal()
    clear_background_markers_signal = QtCore.pyqtSignal()

    data_available_signal = QtCore.pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Data trimming controls
        trim_label = QtWidgets.QLabel(TRIM_TEXT)
        trim_label.setWordWrap(True)
        trim_label.setAlignment(QtCore.Qt.AlignJustify)

        show_trim_bounds_btn = QtWidgets.QPushButton("Enable trim")
        show_trim_bounds_btn.setCheckable(True)
        show_trim_bounds_btn.toggled.connect(self.show_trim_widget)

        trigger_trim_btn = QtWidgets.QPushButton("Trim to bounds")
        trigger_trim_btn.clicked.connect(self.trim_bounds_signal)
        trigger_trim_btn.clicked.connect(lambda: show_trim_bounds_btn.setChecked(False))
        show_trim_bounds_btn.toggled.connect(trigger_trim_btn.setEnabled)
        trigger_trim_btn.setEnabled(False)

        data_controls_layout = QtWidgets.QVBoxLayout()
        data_controls_layout.addWidget(trim_label)
        btns = QtWidgets.QHBoxLayout()
        btns.addWidget(show_trim_bounds_btn)
        btns.addWidget(trigger_trim_btn)
        data_controls_layout.addLayout(btns)

        # Background-only markers
        background_markers_label = QtWidgets.QLabel(BACKGROUND_MARKER_TEXT)
        background_markers_label.setWordWrap(True)
        background_markers_label.setAlignment(QtCore.Qt.AlignJustify)

        add_background_marker_btn = QtWidgets.QPushButton("Add background marker", self)
        add_background_marker_btn.clicked.connect(self.add_background_marker_signal)

        clear_background_markers_btn = QtWidgets.QPushButton(
            "Clear background markers", self
        )
        clear_background_markers_btn.clicked.connect(
            self.clear_background_markers_signal
        )

        background_marker_layout = QtWidgets.QGridLayout()
        background_marker_layout.addWidget(background_markers_label, 0, 0, 1, 2)
        background_marker_layout.addWidget(add_background_marker_btn, 1, 0, 1, 1)
        background_marker_layout.addWidget(clear_background_markers_btn, 1, 1, 1, 1)

        self.first_stage_cb = QtWidgets.QComboBox()
        self.first_stage_cb.addItems(ALL_FIRST_STAGE)
        if "sym6" in ALL_FIRST_STAGE:
            self.first_stage_cb.setCurrentText("sym6")

        self.wavelet_cb = QtWidgets.QComboBox()
        self.wavelet_cb.addItems(ALL_COMPLEX_WAV)
        if "qshift3" in ALL_COMPLEX_WAV:
            self.wavelet_cb.setCurrentText("qshift3")

        self.mode_cb = QtWidgets.QComboBox()
        self.mode_cb.addItems(Modes.modes)
        if "smooth" in Modes.modes:
            self.mode_cb.setCurrentText("constant")

        self.max_iter_widget = QtWidgets.QSpinBox()
        self.max_iter_widget.setRange(0, 1000)
        self.max_iter_widget.setValue(100)

        self.level_widget = QtWidgets.QSpinBox()
        self.level_widget.setMinimum(0)
        self.level_widget.setValue(1)

        self.compute_baseline_btn = QtWidgets.QPushButton(
            "Compute baseline", parent=self
        )
        self.compute_baseline_btn.clicked.connect(
            lambda _: self.baseline_parameters_signal.emit(self.baseline_parameters())
        )

        baseline_controls = QtWidgets.QFormLayout()
        baseline_controls.addRow("First stage wavelet: ", self.first_stage_cb)
        baseline_controls.addRow("Dual-tree wavelet: ", self.wavelet_cb)
        baseline_controls.addRow("Extensions mode: ", self.mode_cb)
        baseline_controls.addRow("Iterations: ", self.max_iter_widget)
        baseline_controls.addRow("Decomposition level: ", self.level_widget)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(data_controls_layout)
        layout.addLayout(background_marker_layout)
        layout.addLayout(baseline_controls)
        layout.addWidget(self.compute_baseline_btn)
        layout.addStretch(1)

        self.setLayout(layout)
        self.resize(self.minimumSize())

    def baseline_parameters(self):
        """ Returns a dictionary of baseline-computation parameters """
        return {
            "first_stage": self.first_stage_cb.currentText(),
            "wavelet": self.wavelet_cb.currentText(),
            "mode": self.mode_cb.currentText(),
            "max_iter": self.max_iter_widget.value(),
            "level": self.level_widget.value(),
        }
