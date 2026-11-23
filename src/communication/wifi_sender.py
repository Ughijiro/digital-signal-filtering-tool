import socket
from src.communication.uart import create_message
from src.butterworth import butterworth_lowpass

HOST = "192.168.1.104"
PORT = 5000

# Calculate real Butterworth Low Pass coefficients.
b, a = butterworth_lowpass(1000, 3, 48000)

print("Original b:", b)
print("Original a:", a)

message = create_message(b, a)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST,PORT))

client.sendall(message)
client.close()

print("success!!")
print("bytes sent: ", len(message))
