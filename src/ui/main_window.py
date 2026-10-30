# Purpose: Create the GUI for the Digital Signal Filtering Tool.
# The interface supports four Butterworth digital filter types.
# Frequencies are displayed in kHz.

import numpy as np

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QSpinBox,
    QDoubleSpinBox,
    QPushButton,
    QMessageBox
)

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from butterworth import (
    butterworth_lowpass,
    butterworth_highpass,
    butterworth_bandpass,
    butterworth_bandstop
)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Purpose: Configure the main application window.
        self.setWindowTitle("Digital Signal Filtering Tool")
        self.resize(800, 480)

        # Purpose: Improve readability and touchscreen usability.
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f6fa;
            }

            QLabel {
                color: #1f2937;
                font-size: 14px;
            }

            QComboBox, QSpinBox, QDoubleSpinBox {
                color: #1f2937;
                background-color: white;
                border: 1px solid #cbd5e1;
                border-radius: 5px;
                padding: 4px;
            }

            QComboBox, QSpinBox, QDoubleSpinBox, QPushButton {
                font-size: 14px;
                min-height: 35px;
                padding: 4px;
            }

            QPushButton {
                background-color: #2563eb;
                color: white;
                border-radius: 6px;
            }

            QPushButton:hover {
                background-color: #1d4ed8;
            }

            QComboBox QAbstractItemView {
                background-color: white;
                color: #1f2937;
                selection-background-color: #2563eb;
                selection-color: white;
            }

            QMessageBox {
                background-color: #f5f6fa;
            }

            QMessageBox QLabel {
                color: #1f2937;
            }

            QMessageBox QPushButton {
                background-color: #2563eb;
                color: white;
                min-width: 70px;
                min-height: 30px;
            }
        """)

        # MAIN LAYOUT

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        # Left side: filter controls.
        layout = QVBoxLayout()
        main_layout.addLayout(layout, 1)

        # Right side: frequency response graph.
        graph_layout = QVBoxLayout()
        main_layout.addLayout(graph_layout, 2)

        # FILTER CONTROLS

        title = QLabel("Digital Filter Designer")
        layout.addWidget(title)

        # Purpose: Select the filter type.
        filter_label = QLabel("Filter Type:")
        layout.addWidget(filter_label)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems([
            "Low Pass",
            "High Pass",
            "Band Pass",
            "Band Stop"
        ])
        layout.addWidget(self.filter_combo)

        # Purpose: Select the cutoff frequency in kHz.
        frequency_label = QLabel("Cutoff Frequency (kHz):")
        layout.addWidget(frequency_label)

        self.frequency_input = QDoubleSpinBox()
        self.frequency_input.setRange(0.01, 20.00)
        self.frequency_input.setDecimals(2)
        self.frequency_input.setSingleStep(0.10)
        self.frequency_input.setValue(1.00)
        layout.addWidget(self.frequency_input)

        # Purpose: Select the upper cutoff frequency
        # for Band Pass and Band Stop filters.
        self.frequency2_label = QLabel(
            "Upper Cutoff Frequency (kHz):"
        )
        layout.addWidget(self.frequency2_label)

        self.frequency2_input = QDoubleSpinBox()
        self.frequency2_input.setRange(0.01, 20.00)
        self.frequency2_input.setDecimals(2)
        self.frequency2_input.setSingleStep(0.10)
        self.frequency2_input.setValue(3.00)
        layout.addWidget(self.frequency2_input)

        # Hide the second cutoff by default.
        self.frequency2_label.hide()
        self.frequency2_input.hide()

        # Purpose: Select the Butterworth prototype order.
        order_label = QLabel("Filter Order:")
        layout.addWidget(order_label)

        self.order_input = QSpinBox()
        self.order_input.setRange(1, 4)
        self.order_input.setValue(2)
        layout.addWidget(self.order_input)

        # Purpose: Design the selected filter.
        self.design_button = QPushButton("Design Filter")
        layout.addWidget(self.design_button)

        self.design_button.clicked.connect(self.design_filter)

        layout.addStretch()

        # FREQUENCY RESPONSE GRAPH

        graph_title = QLabel("Frequency Response")
        graph_layout.addWidget(graph_title)

        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvasQTAgg(self.figure)
        graph_layout.addWidget(self.canvas)

        # Show the second cutoff only for band filters.
        self.filter_combo.currentTextChanged.connect(
            self.update_filter_fields
        )

        # Display an initial Low Pass graph.
        self.update_graph("Low Pass", 1.00)

    # FILTER TYPE SELECTION

    def update_filter_fields(self, filter_type):

        is_band_filter = filter_type in ["Band Pass", "Band Stop"]

        self.frequency2_label.setVisible(is_band_filter)
        self.frequency2_input.setVisible(is_band_filter)

    # DESIGN FILTER BUTTON

    def design_filter(self):

        # Read user-selected parameters.
        filter_type = self.filter_combo.currentText()
        cutoff = self.frequency_input.value()
        upper = self.frequency2_input.value()
        order = self.order_input.value()

        # Validate the frequencies for band filters.
        if filter_type in ["Band Pass", "Band Stop"]:

            if cutoff >= upper:
                QMessageBox.warning(
                    self,
                    "Invalid Frequencies",
                    "The lower cutoff frequency must be smaller "
                    "than the upper cutoff frequency."
                )
                return

        # Display the selected parameters.
        print("Filter:", filter_type)
        print("Cutoff Frequency:", cutoff, "kHz")

        if filter_type in ["Band Pass", "Band Stop"]:
            print("Upper Cutoff Frequency:", upper, "kHz")

        print("Order:", order)
        print("--------------------")

        # Update the frequency response graph.
        self.update_graph(filter_type, cutoff)

    # FREQUENCY RESPONSE

    def update_graph(self, filter_type, cutoff):

        # Generate 500 frequency points from 0 to 20 kHz.
        frequency = np.linspace(0, 20, 500)

        # Convert cutoff frequencies from kHz to Hz.
        cutoff_hz = cutoff * 1000
        upper_hz = self.frequency2_input.value() * 1000

        order = self.order_input.value()
        sampling_hz = 48000

        # CALCULATE FILTER COEFFICIENTS

        if filter_type == "Low Pass":

            b, a = butterworth_lowpass(
                cutoff_hz, order, sampling_hz
            )

        elif filter_type == "High Pass":

            b, a = butterworth_highpass(
                cutoff_hz, order, sampling_hz
            )

        elif filter_type == "Band Pass":

            b, a = butterworth_bandpass(
                cutoff_hz, upper_hz, order, sampling_hz
            )

        elif filter_type == "Band Stop":

            b, a = butterworth_bandstop(
                cutoff_hz, upper_hz, order, sampling_hz
            )

        else:
            return

        # CALCULATE FREQUENCY RESPONSE

        # Convert frequencies to digital angular frequency.
        omega = 2 * np.pi * (frequency * 1000) / sampling_hz

        # Evaluate H(e^jw) using all coefficients.
        numerator = np.zeros(len(frequency), dtype=complex)
        denominator = np.zeros(len(frequency), dtype=complex)

        for i in range(len(b)):
            numerator += b[i] * np.exp(-1j * omega * i)

        for i in range(len(a)):
            denominator += a[i] * np.exp(-1j * omega * i)

        magnitude = np.abs(numerator / denominator)

        # DISPLAY GRAPH

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        ax.plot(frequency, magnitude)

        ax.set_title(f"Butterworth {filter_type} - Order {order}")
        ax.set_xlabel("Frequency (kHz)")
        ax.set_ylabel("Magnitude")
        ax.set_ylim(0, 1.1)
        ax.grid(True)

        self.figure.tight_layout()
        self.canvas.draw()
