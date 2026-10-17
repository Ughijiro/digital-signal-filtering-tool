# Digital Signal Filtering Tool

Bachelor thesis project – Politehnica University of Timișoara.

## 1. Project Overview

A digital filter design application running on a Raspberry Pi 5 with a touchscreen interface.

The user will be able to configure digital filters, calculate their coefficients, and transmit them via UART to a Blackfin DSP processor for real-time audio filtering.

## 2. Hardware

- Raspberry Pi 5 (4 GB RAM)
- 5-inch touchscreen (800 × 480)
- Analog Devices Blackfin DSP board (model to be confirmed)

## 3. Technologies

| Technology | Purpose |
|---|---|
| Python 3.12.7 | Main programming language (development environment) |
| VS Code | Development environment |
| Git & GitHub | Version control |
| PySide6 | Graphical user interface (planned) |
| NumPy & SciPy | Digital filter design and calculations (planned) |
| Matplotlib | Filter response visualization (planned) |
| pySerial | UART communication (planned) |

## 4. Supported Filters

- Low-Pass Filter (LPF)
- High-Pass Filter (HPF)
- Band-Pass Filter (BPF)
- Band-Stop Filter (BSF)

## 5. Development Progress

- [x] Created GitHub repository
- [x] Created project folder structure
- [x] Created Python virtual environment
- [ ] Implement graphical interface
- [ ] Implement filter design
- [ ] Implement frequency response visualization
- [ ] Implement UART communication
- [ ] Integrate Raspberry Pi and Blackfin
- [ ] Test complete system

## 6. Development Notes

The application is initially developed on Windows using VS Code and will later be deployed on Raspberry Pi 5.

The Blackfin DSP receives the audio signal and performs filtering. The Raspberry Pi calculates the filter coefficients and sends them to Blackfin via UART.

Reference code for UART communication was provided from a previous real-time audio watermarking project.