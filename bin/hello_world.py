#!/usr/env/python

import logging
import socket
import threading

from py_client import udp_client

logging.basicConfig(level=logging.DEBUG)

UDP_IP = "192.168.1.136"
UDP_PORT = 4446

USERNAME = b"botty_asldkfj"

logging.debug(f"UDP target IP: {UDP_IP}")
logging.debug(f"UDP target port: {UDP_PORT}")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

listener = threading.Thread(
    target=udp_client.udp_listen,
    kwargs={"sock": sock, "username": USERNAME, "ip": UDP_IP, "port": UDP_PORT},
)
listener.start()

udp_client.send_register(username=USERNAME, sock=sock, ip=UDP_IP, port=UDP_PORT)
