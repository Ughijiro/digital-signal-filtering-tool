
# Purpose: Test UART transmission and reconstruction
# of Butterworth filter coefficients.

import sys
import struct
from pathlib import Path

import serial
import numpy as np

# Add src folder to Python's import path.
sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from communication.uart import send_data, create_message
from butterworth import butterworth_lowpass, butterworth_bandpass


# Calculate Butterworth coefficients.
b, a = butterworth_bandpass(1000, 3000, 4)

# Create binary UART message.
message = create_message(b, a)

# Create virtual UART connection.
uart = serial.serial_for_url("loop://", timeout=1)

try:
    uart.write(message)
    received = uart.read(len(message))
finally:
    uart.close()
    
# Simulate corrupted UART data
""" received = bytearray(received)
received[10] ^= 0x01
received = bytes(received) """
    
# Simulate an incomplete message
# received = received[:-10]

print("Transmission successful:", message == received)


# Check minimum message length.
if len(received) < 6:
    raise ValueError("UART message too short")

# Check header.
if received[:4] != bytes([0xAA, 0xBB, 0xCC, 0xDD]):
    raise ValueError("Invalid UART header")

# Read coefficient counts.
b_count = received[4]
a_count = received[5]

coefficient_count = b_count + a_count

# Verify message length.
expected_length = 6 + 8 * coefficient_count + 1

if len(received) != expected_length:
    raise ValueError("Incomplete or invalid UART message")

received_checksum = received[-1]

calculated_checksum = sum(received[4:-1]) % 256

if received_checksum != calculated_checksum:
    raise ValueError("Checksum value wrong error")

# Reconstruct coefficients.
received_payload = received[6:-1]

decoded = struct.unpack(
    "<" + "d" * coefficient_count,
    received_payload
)

received_b = decoded[:b_count]
received_a = decoded[b_count:]

# Verify coefficients.
print("b match:", np.array_equal(b, received_b))
print("a match:", np.array_equal(a, received_a))


# Test the separate UART transmission function.
bytes_sent = send_data(message)

print("Write successful:", bytes_sent == len(message))
