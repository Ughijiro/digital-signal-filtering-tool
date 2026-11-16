# Digital Signal Filtering Tool

Bachelor thesis project – Politehnica University of Timișoara.

## About the Project

A digital filter design application developed for Raspberry Pi 5 with a touchscreen interface.

The Raspberry Pi is responsible for the user interface and filter coefficient calculations. The coefficients will be transmitted through UART to a Blackfin DSP, which will perform real-time audio filtering.

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
- **C** – UART receiver implementation and testing
- **GCC** – Compilation and testing of the C receiver on Windows
- **Git & GitHub** – Version control

Development is currently performed on Windows using VS Code.

## Current Progress

### Graphical Interface

- Created an 800 × 480 interface for the Raspberry Pi touchscreen.
- Added filter type selection, cutoff frequencies in kHz and filter order.
- Added input validation for band filters.
- Integrated Matplotlib to display frequency response graphs.
- Added a "Send to Blackfin" button.
- Connected the GUI to the UART communication module.
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

### UART Communication — Python

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
- Binary serialization using `struct.pack()`
- UART transmission using pySerial
- Virtual loopback testing using `loop://`
- Message length validation
- Header validation
- Checksum validation
- Reconstruction of transmitted coefficients
- Integration with the graphical interface
- Serial port error handling

### UART Receiver — C

Implemented a standalone UART receiver in C, based on the UART communication examples provided by the thesis supervisor.

The receiver uses a finite state machine to process incoming bytes.

Implemented:
- Detection of the AA BB CC DD header
- Reading numerator and denominator coefficient counts
- Dynamic payload length calculation
- Reception of individual bytes into a buffer
- Buffer size validation (maximum payload: 144 bytes)
- Checksum calculation and verification
- Reconstruction of coefficients using `memcpy()`
- Retrieval of numerator and denominator coefficients
- Processing of consecutive UART messages
- Recovery after complete messages with invalid checksums
- Counting successfully checksum-validated messages

The receiver is currently tested as a standalone C implementation on Windows. Integration into the Blackfin firmware has not yet been performed.

### UART Testing

**Python tests:**
- Low Pass, order 3 — PASS
- Low Pass, order 4 — PASS
- Band Pass, order 4 — PASS
- Incomplete message detection — PASS
- Corrupted message detection — PASS
- Virtual UART transmission — PASS
- GUI-based virtual transmission — PASS
- Unavailable serial port handling — PASS

**C receiver tests:**
- Header detection — PASS
- Coefficient count extraction — PASS
- Checksum verification — PASS
- Python-to-C coefficient reconstruction — PASS
- Automatic comparison of 18 Band Pass coefficients — PASS
- Corrupted message rejection — PASS
- Incomplete message rejection in a standalone test — PASS
- Two consecutive valid messages — PASS
- Corrupted message followed by a valid message — PASS

Test data is generated using Python and saved in binary files. The C receiver reads these files byte by byte to simulate UART reception.

Reference coefficients are also exported from Python and compared against the values reconstructed in C.

**Current limitations:**
- Tests have been performed on Windows without physical UART communication.
- The C receiver has not yet been integrated with the Blackfin UART interrupt handler.
- Automatic timeout and recovery from interrupted transmissions are not implemented.
- A checksum match does not guarantee that the coefficient values are valid for filtering.
- Numerical representation and byte-order compatibility with Blackfin still require verification.
- The physical Raspberry Pi-to-Blackfin communication has not been tested.
- Real-time audio filtering using the received coefficients has not yet been implemented.

## Project Structure

```text
digital-signal-filtering-tool/
├── src/
│   ├── main.py
│   ├── butterworth.py
│   ├── communication/
│   │   ├── uart.py
│   │   └── uart_receiver.c
│   └── ui/
│       └── main_window.py
├── tests/
│   ├── uart_test.py
│   └── uart_receiver_test.c
├── docs/
├── assets/
└── README.md
```

The UART tests also generate local files such as `packet.bin` and `coefficients_reference.txt`.

## Running the Application

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run the application:

```powershell
python src/main.py
```

Test the Python UART communication:

```powershell
python tests/uart_test.py
```

Compile the C UART receiver test:

```powershell
gcc -std=c11 -Wall -Wextra tests/uart_receiver_test.c src/communication/uart_receiver.c -o tests/uart_receiver_test.exe
```

Run the C test:

```powershell
.\tests\uart_receiver_test.exe
```

To test the Butterworth algorithm separately:

```powershell
python src/butterworth.py
```

The UART communication currently uses the virtual `loop://` port by default. Physical UART transmission will be configured during hardware integration.

## Next Steps

### 1. Raspberry Pi Setup

- Prepare and configure Raspberry Pi OS.
- Connect and configure the touchscreen.
- Clone the project from GitHub.
- Install the required Python dependencies.
- Run and test the graphical interface.
- Verify virtual UART communication on Raspberry Pi.

### 2. Blackfin Integration

- Adapt the standalone C receiver to the Blackfin environment.
- Integrate reception with the UART interrupt handler.
- Verify baud rate and numerical representation compatibility.
- Implement receiver timeout handling and improved error recovery.
- Validate received coefficients before applying them.
- Safely update coefficients used by the audio filtering algorithm.

### 3. Physical UART Communication

- Configure Raspberry Pi UART pins.
- Establish the physical Raspberry Pi-to-Blackfin connection.
- Verify actual transmission and reception.
- Test different filter types and orders.
- Verify that Blackfin receives the correct coefficients.

### 4. Real-Time Audio Filtering

- Integrate received coefficients into the audio processing code.
- Implement real-time digital filtering on Blackfin.
- Test the audio input and output.
- Verify filter behavior using different parameters.

### 5. Further Improvements

- Improve UART protocol robustness.
- Perform additional tests for all supported filter types and orders.
- Consider additional filter families after completing the main functionality.
- Improve documentation and testing.

## References

- [Butterworth Lowpass Design – Julius O. Smith III](https://www.dsprelated.com/freebooks/filters/Butterworth_Lowpass_Design.html)
- [Bilinear Transformation – Julius O. Smith III](https://www.dsprelated.com/freebooks/filters/Bilinear_Transformation.html)
- [SciPy Signal Documentation](https://docs.scipy.org/doc/scipy/reference/signal.html)
- [pySerial Documentation](https://pyserial.readthedocs.io/)
