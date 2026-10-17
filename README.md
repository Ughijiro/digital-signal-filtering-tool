# Digital Signal Filtering Tool

Bachelor thesis project – Politehnica University of Timișoara.

## Project Description

A digital filter design application developed for Raspberry Pi 5 with a touchscreen interface.

The Raspberry Pi calculates digital filter coefficients and sends them via UART to a Blackfin DSP, which performs real-time audio filtering.

Supported filter types:
- Low Pass (LPF)
- High Pass (HPF)
- Band Pass (BPF)
- Band Stop (BSF)

## Technologies

- **Python 3.12.7** – Main programming language
- **VS Code** – Development environment
- **PySide6** – Graphical user interface
- **Git & GitHub** – Version control
- **NumPy / SciPy** – Filter design (planned)
- **Matplotlib** – Frequency response visualization (planned)
- **pySerial** – UART communication (planned)

## Project Structure

- `src/main.py` – Application entry point
- `src/ui/` – Graphical interface
- `src/filters/` – Filter coefficient calculations
- `src/analysis/` – Frequency response analysis
- `src/communication/` – UART communication
- `src/config/` – Configuration
- `tests/` – Testing
- `docs/` – Technical notes
- `assets/` – Application resources

## Development Log

### 17 October 2026 – Initial Setup and GUI

**Environment**
- Created GitHub repository and project folders.
- Created Python virtual environment (`.venv`).
- Installed PySide6.
- Updated pip to version 26.2.1.

**GUI Implementation**
- Created the main application window (800 × 480).
- Separated `main.py` from `ui/main_window.py`.
- Added filter selection using `QComboBox`.
- Added cutoff frequency and filter order inputs using `QSpinBox`.
- Implemented dynamic visibility of the second cutoff frequency for BPF and BSF.
- Added the `Design Filter` button using `QPushButton`.
- Connected the button to a function that prints the selected parameters.

**Git**
- Committed and pushed the initial implementation.


**GUI Layout and Visualization**
- Organized the GUI into two columns using QHBoxLayout.
- Applied Qt stylesheets for improved touchscreen usability.
- Fixed text colors for dropdown menus and warning dialogs.
- Installed NumPy and Matplotlib.
- Integrated Matplotlib into PySide6 using FigureCanvasQTAgg.
- Added demonstration magnitude response graphs for LPF, HPF, BPF and BSF.
- Connected the Design Filter button to graph updates.
- Added cutoff frequency validation for band filters.

**Technical Notes**
- The frequency response curves are currently demonstrations, not calculated from actual filter coefficients.
- Filter coefficient calculation and UART communication are not yet implemented.
```


## Running the Application

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run the application:

```powershell
python src/main.py
```

## Next Steps

- Improve the GUI layout for the 800 × 480 touchscreen.
- Add an area for frequency response graphs.
- Prepare the GUI for filter coefficient calculation.
- Study the UART reference code provided by the coordinator.