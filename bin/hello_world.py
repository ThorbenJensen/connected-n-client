#!/usr/env/python

import logging

from py_client.udp_client import UdpClient

logging.basicConfig(level=logging.DEBUG)

USERNAME = b"botty_asldkfj"
UDP_IP = "192.168.1.136"
UDP_PORT = 4446

c = UdpClient(username=USERNAME, ip=UDP_IP, port=UDP_PORT)

c.init_socket()
c.start_listener()

c.send_register()
