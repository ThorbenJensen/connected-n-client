""" General player class. """

import logging
import random

logging.basicConfig(level=logging.DEBUG)


class Player:
    """Super-class for players."""
    def choose_action(self) -> int:
        logging.debug("Choosing new action...")
        return 3

    def inform(self, column: int, opponent: bool):
        """Informs about the previous move
        Arguments:
            column {int} -- Column of previous move.
            opponent {bool} -- If previous move was taken out by opponent.
        """
        pass

    def reset(self):
        pass


class RandomPlayer(Player):
    def choose_action(self) -> int:
        return random.randrange(0, 7)

    def inform(self, column: int, opponent: bool):
        pass

    def reset(self):
        pass
