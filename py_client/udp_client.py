""" UDP client in python. """

import random

def send_register(username, sock, ip, port):
    message = b"REGISTER;" + username
    sock.sendto(message, (ip, port))


def send_join(season, sock, ip, port):
    message = b"JOIN;" + season
    sock.sendto(message, (ip, port))


def send_insert(column, token, sock, ip, port):
    message = b"INSERT;" + str(column).encode() + b";" + token
    sock.sendto(message, (ip, port))


def receive_welcome(message):
    # Expect: WELCOME;$username
    print("Computer sagt ja.")

def receive_new_season(data, sock, ip, port):
    # Expect: NEW SEASON;$season
    season = data[0]
    send_join(season, sock, ip, port)

def receive_new_game(data):
    # Expect: NEW GAME;$opponent
    pass


def receive_yourturn(data, sock, ip, port):
    # Expect: YOURTURN;$token
    token = data[0]
    column = random.randrange(0, 7)
    send_insert(column, token, sock, ip, port)
    pass


def udp_listen(sock, ip, port):
    while True:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        print("received message:", data)
        message = data.split(b";")

        if message[0] == b"WELCOME":
            receive_welcome(message[1:])
        elif message[0] == b"NEW SEASON":
            receive_new_season(message[1:], sock, ip, port)
        elif message[0] == b"NEW GAME":
            receive_new_game(message[1:])
        elif message[0] == b"YOURTURN":
            receive_yourturn(message[1:], sock, ip, port)