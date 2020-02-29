""" UDP client in python. """

import socket

UDP_IP = "192.168.1.136"
UDP_PORT = 4446

USERNAME = b"botty_asldkfj"

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
# print("message:", MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
# sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

def register(username):
    message = b"REGISTER;" + username
    sock.sendto(message, (UDP_IP, UDP_PORT))

register(USERNAME)

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print("received message:", data)