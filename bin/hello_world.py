#!/usr/env/python

from py_client import udp_client

import socket
import threading

UDP_IP = "192.168.1.136"
UDP_PORT = 4446

USERNAME = b"botty_asldkfj"

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP

listener = threading.Thread(target=udp_client.udp_listen, args=[sock])
listener.start()

udp_client.send_register(username=USERNAME, sock=sock, ip=UDP_IP, port=UDP_PORT)
