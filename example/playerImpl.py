""" Example player implementation class"""
from random import random

from py_client.player import Player


class PlayerImpl(Player):
    def choose_action(self) -> int:
        return random.randrange(0, 7)

    def inform(self, column: int, opponent: bool):
        pass

    def reset(self):
        pass