""" UDP client in python. """

import logging
import random
import socket
import threading

logging.basicConfig(level=logging.DEBUG)


class UdpClient:
    """UDP client for playing Connect-N"""

    def __init__(self, username: str, ip: str, port: int):
        self._username: str = username
        self._ip: str = ip
        self._port: int = port
        # reserve opponent
        self._opponent = None
        # prepare game
        self.init_socket()
        self.start_listener()

    # SETTING UP
    def init_socket(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start_listener(self):
        logging.debug("Starting listerner...")
        listener = threading.Thread(target=self.udp_listen)
        listener.start()

    # LISTENING
    def udp_listen(self):
        while True:
            data, addr = self._socket.recvfrom(1024)  # buffer size is 1024 bytes
            logging.debug(f"received message: {data}")
            message = data.split(b";")

            if message[0] == b"WELCOME":
                self.receive_welcome(username=message[1].decode())
            elif message[0] == b"NEW SEASON":
                self.receive_new_season(season=message[1].decode())
            elif message[0] == b"NEW GAME":
                self.receive_new_game(opponent=message[1].decode())
            elif message[0] == b"YOURTURN":
                self.receive_yourturn(token=message[1].decode())
            elif message[0] == b"TOKEN INSERTED":
                self.receive_token_inserted(
                    player=message[1].decode(), column=int(message[2].decode())
                )
            # error handling
            # elif message[-1].startswith(b"No response for UUID"):
            #     logging.debug("No response error! Restarting client...")
            #     self.send_register()

    # RECEIVING
    def receive_welcome(self, username: str):
        # Expect: WELCOME;$username
        logging.debug("Computer sagt ja.")

    def receive_new_season(self, season: str):
        # Expect: NEW SEASON;$season
        self.send_join(season)

    def receive_new_game(self, opponent: str):
        # Expect: NEW GAME;$opponent
        self._opponent = opponent

    def receive_yourturn(self, token: str):
        # Expect: YOURTURN;$token
        column = random.randrange(0, 7)
        logging.debug(f"Inserting into {column}")
        self.send_insert(column=column, token=token)

    def receive_token_inserted(self, player: str, column: int):
        # Expect: TOKEN INSERTED;$player;$column
        is_opponent = False if player == self._username else True
        if is_opponent:
            logging.debug(f"Opponent inserted into {column}")

    # SENDING
    def send_udp_message(self, message: str):
        self._socket.sendto(message.encode(), (self._ip, self._port))

    def send_register(self):
        logging.debug("Registering with server...")
        message = f"REGISTER;{self._username}"
        self.send_udp_message(message)

    def send_join(self, season):
        message = f"JOIN;{season}"
        self.send_udp_message(message)

    def send_insert(self, column: int, token):
        message = f"INSERT;{column};{token}"
        self.send_udp_message(message)
