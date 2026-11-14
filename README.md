
# Digital Signal Filtering Tool

Bachelor thesis project – Politehnica University of Timișoara.

## About the Project

A digital filter design application developed for Raspberry Pi 5 with a touchscreen interface.

The Raspberry Pi is responsible for the user interface and filter coefficient calculations. The coefficients are sent through UART to a Blackfin DSP, which performs real-time audio filtering.

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
- **pySerial** – UART communication and virtual testing
- **C** – Planned Blackfin receiver implementation
- **Git & GitHub** – Version control

Development is currently done on Windows using VS Code.

## Current Progress

### Graphical Interface

- Created an 800 × 480 interface for the Raspberry Pi touchscreen.
- Added filter type selection, cutoff frequencies in kHz and filter order.
- Added input validation for band filters.
- Integrated Matplotlib to display frequency response graphs.
- Added a "Send to Blackfin" button.
- Added success and error messages for UART transmission.
- Disabled UART transmission when filter parameters change, until the filter is designed again.

### Filter Design

- Implemented Butterworth Low Pass, High Pass, Band Pass and Band Stop.
- Added support for prototype orders 1–4.
- Implemented pole calculations, frequency prewarping and bilinear transformation.
- Calculated digital filter coefficients without using SciPy design functions.
- Verified all four filter types against SciPy for orders 1–4.
- Connected all filters to the GUI and tested their frequency responses.
- Sampling frequency is currently fixed at 48 kHz.

### UART Communication

Implemented binary message construction and virtual UART transmission using Python and pySerial.

Message structure:
- Header: 4 bytes (AA BB CC DD)
- B_COUNT: number of numerator coefficients (1 byte)
- A_COUNT: number of denominator coefficients (1 byte)
- Payload: filter coefficients stored as 64-bit little-endian doubles
- Checksum: 1 byte

The checksum is calculated as the sum of the count and payload bytes modulo 256.

Implemented:
- Dynamic coefficient counts
- Binary serialization using struct.pack()
- UART transmission using pySerial
- Virtual loopback testing with loop://
- Message length validation
- Header validation
- Checksum validation
- Reconstruction of transmitted coefficients
- Integration with the graphical interface
- Serial port error handling

### UART Tests

Successfully tested:
- Low Pass, order 3
- Low Pass, order 4
- Band Pass, order 4
- Detection of incomplete messages
- Detection of corrupted message data
- Handling of unavailable serial ports
- GUI-based virtual UART transmission

The reconstructed coefficients matched the original values in the completed tests.

Current limitations:
- Tests were performed on Windows without physical UART hardware.
- The Blackfin receiver has not yet been adapted to the new protocol.
- Byte-by-byte reception, buffering and timeout handling still need to be implemented.
- The final numeric format and baud rate must be verified for Blackfin compatibility.
- Real Raspberry Pi to Blackfin communication has not yet been tested.

## Project Structure

digital-signal-filtering-tool/
├── src/
│   ├── main.py
│   ├── butterworth.py
│   ├── communication/
│   │   └── uart.py
│   └── ui/
│       └── main_window.py
├── tests/
│   └── uart_test.py
├── docs/
├── assets/
└── README.md

## Running the Application

Activate the virtual environment:

    .\.venv\Scripts\Activate.ps1

Run the application:

    python src/main.py

To test the UART communication:

    python tests/uart_test.py

To test the Butterworth algorithm separately:

    python src/butterworth.py

## Next Steps

### 1. Blackfin UART Receiver

- Study and adapt the provided C code.
- Implement reception of the new message format.
- Add safe buffer management.
- Detect complete and incomplete messages.
- Validate message length and checksum.
- Reconstruct the filter coefficients.
- Test the receiver logic on the laptop where possible.

### 2. Hardware Integration

- Configure the Raspberry Pi UART interface.
- Connect Raspberry Pi to Blackfin.
- Verify communication settings and numeric compatibility.
- Test physical coefficient transmission.
- Integrate received coefficients into real-time audio filtering.

### 3. Further Improvements

- Improve protocol robustness and error handling.
- Perform additional tests for all filter types and orders.
- Consider additional filter families after completing the main communication functionality.

## References

- [Butterworth Lowpass Design – Julius O. Smith III](https://www.dsprelated.com/freebooks/filters/Butterworth_Lowpass_Design.html)
- [Bilinear Transformation – Julius O. Smith III](https://www.dsprelated.com/freebooks/filters/Bilinear_Transformation.html)
- [SciPy Signal Documentation](https://docs.scipy.org/doc/scipy/reference/signal.html)
- [pySerial Documentation](https://pyserial.readthedocs.io/)
