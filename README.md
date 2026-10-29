# Digital Signal Filtering Tool

Bachelor thesis project – Politehnica University of Timișoara.

## About the Project

A digital filter design application developed for Raspberry Pi 5 with a touchscreen interface.

The Raspberry Pi is responsible for the user interface and filter coefficient calculations. The coefficients will be sent through UART to a Blackfin DSP, which performs real-time audio filtering.

The application supports four filter types:
- Low Pass (LPF)
- High Pass (HPF)
- Band Pass (BPF)
- Band Stop (BSF)

## Technologies

- **Python** – Main programming language
- **PySide6** – Graphical user interface
- **NumPy** – Mathematical calculations
- **Matplotlib** – Frequency response visualization
- **SciPy** – Verification of filter coefficients
- **pySerial** – UART communication (planned)
- **Git & GitHub** – Version control

Development is currently done on Windows using VS Code.

## Current Progress

### Graphical Interface
- Created an 800 × 480 interface for the Raspberry Pi touchscreen.
- Added filter type selection, cutoff frequencies in kHz and filter order.
- Added input validation for band filters.
- Integrated Matplotlib to display frequency response graphs.

### Filter Design
- Implemented a digital Butterworth Low Pass filter for orders 1–4.
- Calculated filter coefficients using mathematical formulas and pole calculations.
- Implemented frequency prewarping and bilinear transformation.
- Verified the calculated coefficients against SciPy.
- Connected the Butterworth Low Pass algorithm to the GUI.
- Confirmed that increasing the filter order produces a steeper transition.

High Pass, Band Pass and Band Stop currently use demonstration curves.

The sampling frequency is temporarily set to 48 kHz.

## Project Structure

```text
digital-signal-filtering-tool/
├── src/
│   ├── main.py
│   ├── butterworth.py
│   └── ui/
│       └── main_window.py
├── tests/
├── docs/
├── assets/
└── README.md
```

Other modules will be added as development continues.

## Running the Application

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run the application:

```powershell
python src/main.py
```

To test the Butterworth algorithm separately:

```powershell
python src/butterworth.py
```

## Next Steps

- Implement Butterworth High Pass, Band Pass and Band Stop.
- Add support for additional filter families, such as Chebyshev.
- Improve filter design and coefficient validation.
- Implement UART communication between Raspberry Pi and Blackfin.
- Test the application on Raspberry Pi 5 with the touchscreen.
- Integrate and test real-time audio filtering on Blackfin.

## References

- [Butterworth Lowpass Design – Julius O. Smith III](https://www.dsprelated.com/freebooks/filters/Butterworth_Lowpass_Design.html)
- [Bilinear Transformation – Julius O. Smith III](https://www.dsprelated.com/freebooks/filters/Bilinear_Transformation.html)
- [SciPy Signal Documentation](https://docs.scipy.org/doc/scipy/reference/signal.html)