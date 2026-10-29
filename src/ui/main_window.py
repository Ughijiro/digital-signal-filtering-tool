# Purpose: Create a graphical interface for designing digital filters.
# The user can select the filter type, cutoff frequencies, and filter order.
# Frequency values are displayed in kHz.
# The frequency response is currently demonstrated using simple formulas.

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

import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from butterworth import butterworth_lowpass


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

            /* Purpose: Fix dropdown list colors. */
            QComboBox QAbstractItemView {
                background-color: white;
                color: #1f2937;
                selection-background-color: #2563eb;
                selection-color: white;
                border: 1px solid #cbd5e1;
            }

            QMessageBox {
                background-color: #f5f6fa;
            }

            QMessageBox QLabel {
                color: #1f2937;
                font-size: 14px;
            }

            QMessageBox QPushButton {
                background-color: #2563eb;
                color: white;
                min-width: 70px;
                min-height: 30px;
            }
        """)

        # Purpose: Create the central widget and main layout.
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Purpose: Split the GUI into controls and graph areas.
        main_layout = QHBoxLayout(central_widget)

        layout = QVBoxLayout()
        main_layout.addLayout(layout, 1)

        graph_layout = QVBoxLayout()
        main_layout.addLayout(graph_layout, 2)

        # -----------------------------------------
        # FILTER CONTROLS
        # -----------------------------------------

        title = QLabel("Digital Filter Designer")
        layout.addWidget(title)

        # Purpose: Allow selection of one of four filter types.
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
        # QDoubleSpinBox allows decimal values such as 1.50 kHz.
        frequency_label = QLabel("Cutoff Frequency (kHz):")
        layout.addWidget(frequency_label)

        self.frequency_input = QDoubleSpinBox()
        self.frequency_input.setRange(0.01, 20.00)
        self.frequency_input.setDecimals(2)
        self.frequency_input.setSingleStep(0.10)
        self.frequency_input.setValue(1.00)
        layout.addWidget(self.frequency_input)

        # Purpose: Add a second cutoff frequency for band filters.
        self.frequency2_label = QLabel("Upper Cutoff Frequency (kHz):")
        layout.addWidget(self.frequency2_label)

        self.frequency2_input = QDoubleSpinBox()
        self.frequency2_input.setRange(0.01, 20.00)
        self.frequency2_input.setDecimals(2)
        self.frequency2_input.setSingleStep(0.10)
        self.frequency2_input.setValue(3.00)
        layout.addWidget(self.frequency2_input)

        # Purpose: Hide the upper cutoff frequency by default.
        self.frequency2_label.hide()
        self.frequency2_input.hide()

        # Purpose: Select the filter order.
        # QSpinBox is used because the order must be an integer.
        order_label = QLabel("Filter Order:")
        layout.addWidget(order_label)

        self.order_input = QSpinBox()
        self.order_input.setRange(1, 100)
        self.order_input.setValue(2)
        layout.addWidget(self.order_input)

        # Purpose: Create a button to design the selected filter.
        self.design_button = QPushButton("Design Filter")
        layout.addWidget(self.design_button)

        self.design_button.clicked.connect(self.design_filter)

        layout.addStretch()

        # -----------------------------------------
        # FREQUENCY RESPONSE GRAPH
        # -----------------------------------------

        # Purpose: Create a graph inside the application window.
        graph_title = QLabel("Frequency Response")
        graph_layout.addWidget(graph_title)

        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvasQTAgg(self.figure)

        graph_layout.addWidget(self.canvas)

        # Purpose: Show the upper cutoff input only for band filters.
        self.filter_combo.currentTextChanged.connect(
            self.update_filter_fields
        )

        # Purpose: Display the initial demonstration graph.
        self.update_graph(
            self.filter_combo.currentText(),
            self.frequency_input.value()
        )

    # -----------------------------------------
    # FILTER TYPE SELECTION
    # -----------------------------------------

    def update_filter_fields(self, filter_type):

        # Purpose: Check whether the selected filter needs two frequencies.
        is_band_filter = filter_type in ["Band Pass", "Band Stop"]

        self.frequency2_label.setVisible(is_band_filter)
        self.frequency2_input.setVisible(is_band_filter)

    # -----------------------------------------
    # FILTER DESIGN BUTTON
    # -----------------------------------------

    def design_filter(self):

        # Purpose: Read the parameters selected by the user.
        filter_type = self.filter_combo.currentText()
        frequency = self.frequency_input.value()
        order = self.order_input.value()
        
        # Purpose: Prevent using unsupported orders for the current algorithm.
        # Purpose: Validate the supported Butterworth Low Pass orders.
        if filter_type == "Low Pass" and not 1 <= order <= 4:
            QMessageBox.warning(
                self,
                "Unsupported Order",
                "Butterworth Low Pass currently supports orders 1 to 4."
            )
            return

        # Purpose: Validate the cutoff frequencies for band filters.
        if filter_type in ["Band Pass", "Band Stop"]:

            upper = self.frequency2_input.value()

            if frequency >= upper:
                QMessageBox.warning(
                    self,
                    "Invalid Frequencies",
                    "The lower cutoff frequency must be smaller "
                    "than the upper cutoff frequency."
                )
                return

        # Purpose: Display the selected parameters in the terminal.
        print("Filter:", filter_type)
        print("Cutoff Frequency:", frequency, "kHz")

        if filter_type in ["Band Pass", "Band Stop"]:
            print(
                "Upper Cutoff Frequency:",
                self.frequency2_input.value(),
                "kHz"
            )

        print("Order:", order)
        print("--------------------")

        # Purpose: Update the frequency response graph.
        self.update_graph(filter_type, frequency)

    # -----------------------------------------
    # DEMONSTRATION FREQUENCY RESPONSE
    # -----------------------------------------

    
    def update_graph(self, filter_type, cutoff):

        # Purpose: Generate 500 frequency points from 0 to 20 kHz.
        frequency = np.linspace(0, 20, 500)

        if filter_type == "Low Pass":

            # Convert kHz to Hz.
            cutoff_hz = cutoff * 1000

            # Read the selected filter order.
            order = self.order_input.value()

            # Calculate Butterworth Low Pass coefficients.
            b, a = butterworth_lowpass(cutoff_hz, order)

            # Convert frequency values to digital angular frequency.
            omega = 2 * np.pi * (frequency * 1000) / 48000

            # Calculate the frequency response using all coefficients.
            numerator = np.zeros(len(frequency), dtype=complex)
            denominator = np.zeros(len(frequency), dtype=complex)

            for i in range(len(b)):
                numerator += b[i] * np.exp(-1j * omega * i)

            for i in range(len(a)):
                denominator += a[i] * np.exp(-1j * omega * i)

            magnitude = np.abs(numerator / denominator)

            # Display calculated coefficients in the terminal.
            print("Butterworth Low Pass coefficients:")
            print("b:", b)
            print("a:", a)

        elif filter_type == "High Pass":

            # Demonstration High Pass response.
            magnitude = (frequency / cutoff) ** 2 / np.sqrt(
                1 + (frequency / cutoff) ** 4
            )

        elif filter_type == "Band Pass":

            # Demonstration Band Pass response.
            upper = self.frequency2_input.value()
            center = (cutoff + upper) / 2
            bandwidth = (upper - cutoff) / 2

            if bandwidth <= 0:
                return

            magnitude = np.exp(
                -0.5 * ((frequency - center) / bandwidth) ** 2
            )

        elif filter_type == "Band Stop":

            # Demonstration Band Stop response.
            upper = self.frequency2_input.value()
            center = (cutoff + upper) / 2
            bandwidth = (upper - cutoff) / 2

            if bandwidth <= 0:
                return

            magnitude = 1 - np.exp(
                -0.5 * ((frequency - center) / bandwidth) ** 2
            )

        # Purpose: Clear the previous graph.
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Purpose: Display the frequency response.
        ax.plot(frequency, magnitude)

        if filter_type == "Low Pass":
            ax.set_title(f"Butterworth Low Pass - Order {order}")
        else:
            ax.set_title(f"{filter_type} - Demonstration")

        ax.set_xlabel("Frequency (kHz)")
        ax.set_ylabel("Magnitude")
        ax.grid(True)

        self.figure.tight_layout()
        self.canvas.draw()
