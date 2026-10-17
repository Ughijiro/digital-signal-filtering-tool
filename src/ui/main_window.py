
# Purpose: Create the main window with a filter selection menu.

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QLabel, QComboBox, QSpinBox, QPushButton
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Digital Signal Filtering Tool")
        self.resize(800, 480)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

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

        print("Filter:", filter_type)
        print("Cutoff Frequency:", frequency)

        if filter_type in ["Band Pass", "Band Stop"]:
            print("Upper Cutoff Frequency:", self.frequency2_input.value())

        print("Order:", order)
        print("--------------------")

