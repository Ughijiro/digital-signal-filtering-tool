# Purpose: Create and transmit binary UART messages.

import serial
import struct


# Send data through a serial connection.
def send_data(message, port="loop://"):

    uart = serial.serial_for_url(
        port,
        baudrate=115200,
        timeout=1
    )

    try:
        bytes_sent = uart.write(message)
        uart.flush()

        return bytes_sent

    finally:
        uart.close()


# Convert filter coefficients into a binary message.
def create_message(b, a):
    
    b_count = len(b)
    a_count = len(a)
    counts_bytes = bytes([b_count, a_count])

    header = bytes([0xAA, 0xBB, 0xCC, 0xDD])

    coefficients = list(b) + list(a)

    payload = struct.pack(
        "<" + "d" * len(coefficients),
        *coefficients
    )
    
    checksum = sum(counts_bytes + payload) % 256
    checksum_bytes = bytes([checksum])
    return header + counts_bytes + payload + checksum_bytes