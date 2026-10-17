# Purpose: Create the main window with a filter selection menu.

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,QHBoxLayout,
    QLabel, QComboBox, QSpinBox, QPushButton,
    QMessageBox
)
from PySide6.QtCore import Qt
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

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

            QComboBox, QSpinBox {
                color: #1f2937;
                background-color: white;
                border: 1px solid #cbd5e1;
                border-radius: 5px;
                padding: 4px;
            }

            QLabel {
                font-size: 14px;
            }

            QComboBox, QSpinBox, QPushButton {
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
            
            /* Purpose: Fix dropdown list colors for filter selection. */

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

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Purpose: Split the GUI into filter controls and visualization areas.
        main_layout = QHBoxLayout(central_widget)

        layout = QVBoxLayout()
        main_layout.addLayout(layout, 1)

        graph_layout = QVBoxLayout()
        main_layout.addLayout(graph_layout, 2)

        title = QLabel("Digital Filter Designer")
        layout.addWidget(title)

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
        
        # Purpose: Add input fields for the filter cutoff frequency and order.

        frequency_label = QLabel("Cutoff Frequency (Hz):")
        layout.addWidget(frequency_label)

        self.frequency_input = QSpinBox()
        self.frequency_input.setRange(1, 20000)
        self.frequency_input.setValue(1000)
        layout.addWidget(self.frequency_input)
        
        
        # Purpose: Add a second cutoff frequency for band filters.

        self.frequency2_label = QLabel("Upper Cutoff Frequency (Hz):")
        layout.addWidget(self.frequency2_label)

        self.frequency2_input = QSpinBox()
        self.frequency2_input.setRange(1, 20000)
        self.frequency2_input.setValue(3000)
        layout.addWidget(self.frequency2_input)

        self.frequency2_label.hide()
        self.frequency2_input.hide()


        order_label = QLabel("Filter Order:")
        layout.addWidget(order_label)

        self.order_input = QSpinBox()
        self.order_input.setRange(1, 100)
        self.order_input.setValue(4)
        layout.addWidget(self.order_input)
        
        # Purpose: Create a button to read the selected filter parameters.

        self.design_button = QPushButton("Design Filter")
        layout.addWidget(self.design_button)

        self.design_button.clicked.connect(self.design_filter)

        layout.addStretch()
        # Placeholder for the future frequency response graph.
        graph_title = QLabel("Frequency Response")
        graph_layout.addWidget(graph_title)

        # Purpose: Display a demonstration frequency response graph.

        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvasQTAgg(self.figure)

        graph_layout.addWidget(self.canvas)

        ax = self.figure.add_subplot(111)

        frequency = np.linspace(0, 20000, 500)
        magnitude = 1 / np.sqrt(1 + (frequency / 3000) ** 4)

        ax.plot(frequency, magnitude)
        ax.set_title("Magnitude Response")
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Magnitude")
        ax.grid(True)

        self.figure.tight_layout()
        self.canvas.draw()
        
        
        # Purpose: Show the second frequency only for band filters.

        self.filter_combo.currentTextChanged.connect(self.update_filter_fields)

    def update_filter_fields(self, filter_type):
        is_band_filter = filter_type in ["Band Pass", "Band Stop"]

        self.frequency2_label.setVisible(is_band_filter)
        self.frequency2_input.setVisible(is_band_filter)
    
    def design_filter(self):
        filter_type = self.filter_combo.currentText()
        frequency = self.frequency_input.value()
        order = self.order_input.value()
        
        # Purpose: Validate cutoff frequencies for band filters.

        if filter_type in ["Band Pass", "Band Stop"]:
            upper = self.frequency2_input.value()

            if frequency >= upper:
                QMessageBox.warning(
                    self,
                    "Invalid Frequencies",
                    "The lower cutoff frequency must be smaller than the upper cutoff frequency."
                )
                return

        print("Filter:", filter_type)
        print("Cutoff Frequency:", frequency)

        if filter_type in ["Band Pass", "Band Stop"]:
            print("Upper Cutoff Frequency:", self.frequency2_input.value())

        print("Order:", order)
        print("--------------------")
        self.update_graph(filter_type, frequency)

    # Purpose: Update the demonstration graph based on the selected filter type.

    def update_graph(self, filter_type, cutoff):
        frequency = np.linspace(0, 20000, 500)

        if filter_type == "Low Pass":
            magnitude = 1 / np.sqrt(1 + (frequency / cutoff) ** 4)

        elif filter_type == "High Pass":
            magnitude = (frequency / cutoff) ** 2 / np.sqrt(
                1 + (frequency / cutoff) ** 4
            )

        # Purpose: Add demonstration curves for Band Pass and Band Stop.

        elif filter_type == "Band Pass":
            upper = self.frequency2_input.value()
            center = (cutoff + upper) / 2
            bandwidth = (upper - cutoff) / 2

            if bandwidth <= 0:
                return

            magnitude = np.exp(-0.5 * ((frequency - center) / bandwidth) ** 2)

        elif filter_type == "Band Stop":
            upper = self.frequency2_input.value()
            center = (cutoff + upper) / 2
            bandwidth = (upper - cutoff) / 2

            if bandwidth <= 0:
                return

            magnitude = 1 - np.exp(
                -0.5 * ((frequency - center) / bandwidth) ** 2
            )
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        ax.plot(frequency, magnitude)
        ax.set_title(f"{filter_type} - Demonstration")
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Magnitude")
        ax.grid(True)

        self.figure.tight_layout()
        self.canvas.draw()
