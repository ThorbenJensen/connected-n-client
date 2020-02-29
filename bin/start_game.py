#!/usr/env/python

import logging

from py_client.udp_client import UdpClient
from py_client.players import RandomPlayer

logging.basicConfig(level=logging.DEBUG)

USERNAME = "botty_asldkfj😃"
UDP_IP = "192.168.1.136"
UDP_PORT = 4446

player = RandomPlayer()

c = UdpClient(username=USERNAME, ip=UDP_IP, port=UDP_PORT, player=player)
c.send_register()
