# Purpose: Test physical UART loopback with Butterworth coefficients.

import serial
import struct

from src.butterworth import butterworth_lowpass
from src.communication.uart import create_message

# Calculate Butterworth Low Pass coefficients.
b, a = butterworth_lowpass(1000, 3, 48000)

# Convert coefficients into a binary UART message.
message = create_message(b, a)

print("Original b:", b)
print("Original a:", a)
print("Message size:", len(message))

# Send and receive the message through physical UART.
port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=1)

port.reset_input_buffer()

bytes_sent = port.write(message)
port.flush()

received = port.read(len(message))

port.close()

print("Bytes sent:", bytes_sent)
print("Bytes received:", len(received))
print("Messages match:", received == message)

# Purpose: Verify the checksum of the received UART message.

received_checksum = received[-1]
calculated_checksum = sum(received[4:-1]) % 256

print("Checksum valid:", received_checksum == calculated_checksum)

# Purpose: Reconstruct Butterworth coefficients from received UART bytes.

b_count = received[4]
a_count = received[5]

coefficients = struct.unpack(
    "<" + "d" * (b_count + a_count),
    received[6:-1]
)

received_b = coefficients[:b_count]
received_a = coefficients[b_count:]

print("Received b:", received_b)
print("Received a:", received_a)

# Purpose: Verify that received coefficients match the originals.
print("b match:", list(b) == list(received_b))
print("a match:", list(a) == list(received_a))