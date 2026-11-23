import socket
import struct 

# Reads exactly the requested number of bytes from TCP.
def receive_exact(connection, size):
    data = b""

    while len(data) < size:
        chunk = connection.recv(size - len(data))

        if not chunk:
            raise ConnectionError("Incomplete message")

        data += chunk

    return data

HOST = "0.0.0.0"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Waiting for Raspberry Pi...")

connection, address = server.accept()

print("Connected:", address)

header = receive_exact(connection, 4)

if header != bytes([0xAA, 0xBB, 0xCC, 0xDD]):
    raise ValueError("Invalid header")

counts = receive_exact(connection, 2)

b_count = counts[0]
a_count = counts[1]

MAX_PAYLOAD_SIZE = 144

if b_count == 0 or a_count == 0:
    raise ValueError("Invalid coefficient count")

payload_size = (b_count + a_count) * 8

if payload_size > MAX_PAYLOAD_SIZE:
    raise ValueError("Payload too large")


payload = receive_exact(connection, payload_size)
checksum = receive_exact(connection, 1)

data = header + counts + payload + checksum
print("Received:", data)

b_count = data[4]
a_count = data[5]

coefficients = struct.unpack(
    "<" + "d" * (b_count + a_count),
    data[6:-1]
)

b = coefficients[:b_count]
a = coefficients[b_count:]

print("b coefficients:", b)
print("a coefficients:", a)

received_checksum = data[-1]
calculated_checksum = sum(data[4:-1]) % 256

if received_checksum != calculated_checksum:
    raise ValueError("Invalid checksum")

print("Checksum valid: True")

connection.close()
server.close()