""" UDP client in python. """

import socket
import threading
import random

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

def send_join(season):
    message = b"JOIN;" + season
    sock.sendto(message, (UDP_IP, UDP_PORT))


def send_insert(column, token):
    message = b"INSERT;" + str(column).encode() + b";" + token
    sock.sendto(message, (UDP_IP, UDP_PORT))
    pass


def receive_welcome(message):
    # Expect: WELCOME;$username
    print("Computer sagt ja.")
    pass

def receive_new_season(data):
    # Expect: NEW SEASON;$season
    season = data[0]
    send_join(season)

def receive_new_game(data):
    # Expect: NEW GAME;$opponent
    pass


def receive_yourturn(data):
    # Expect: YOURTURN;$token
    token = data[0]
    column = random.randrange(0, 7)
    send_insert(column, token)
    pass


def udp_listen():
    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print("received message:", data)
        message = data.split(b";")

        if message[0] == b"WELCOME":
            receive_welcome(message[1:])
        elif message[0] == b"NEW SEASON":
            receive_new_season(message[1:])
        elif message[0] == b"NEW GAME":
            receive_new_game(message[1:])
        elif message[0] == b"YOURTURN":
            receive_yourturn(message[1:])


listener = threading.Thread(target=udp_listen)
listener.start()

send_register(USERNAME)