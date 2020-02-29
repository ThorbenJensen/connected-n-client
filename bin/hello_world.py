#!/usr/env/python

import socket
import threading

UDP_IP = "192.168.1.136"
UDP_PORT = 4446

USERNAME = b"botty_asldkfj"

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

def send_register(username):
    message = b"REGISTER;" + username
    sock.sendto(message, (UDP_IP, UDP_PORT))

def receive_welcome(message):
    # Expect: WELCOME;$username
    print("Computer sagt ja.")
    pass


def receive_new_season(data):
    # Expect: NEW SEASON;$season
    pass


def receive_new_game(data):
    # Expect: NEW GAME;$opponent
    pass


def udp_listen():
    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print("received message:", data)
        if data.startswith(b"WELCOME;"):
            receive_welcome(data)
        elif data.startswith(b"NEW SEASON;"):
            receive_new_season(data)
        elif data.startswith(b"NEW GAME;"):
            receive_new_game(data)


listener = threading.Thread(target=udp_listen)
listener.start()

send_register(USERNAME)
