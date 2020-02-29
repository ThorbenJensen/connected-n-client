""" UDP client in python. """


def send_register(username, sock, ip, port):
    message = b"REGISTER;" + username
    sock.sendto(message, (ip, port))


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


def udp_listen(sock):
    while True:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        print("received message:", data)
        if data.startswith(b"WELCOME;"):
            receive_welcome(data)
        elif data.startswith(b"NEW SEASON;"):
            receive_new_season(data)
        elif data.startswith(b"NEW GAME;"):
            receive_new_game(data)
