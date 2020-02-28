import numpy as np
from random import randint
from datetime import datetime
from py_client.players import Player

row_masks = [
    [0, 0, 4],
    [0, 1, 5],
    [0, 2, 6],
    [0, 3, 7],
    [1, 0, 4],
    [1, 1, 5],
    [1, 2, 6],
    [1, 3, 7],
    [2, 0, 4],
    [2, 1, 5],
    [2, 2, 6],
    [2, 3, 7],
    [3, 0, 4],
    [3, 1, 5],
    [3, 2, 6],
    [3, 3, 7],
    [4, 0, 4],
    [4, 1, 5],
    [4, 2, 6],
    [4, 3, 7],
    [5, 0, 4],
    [5, 1, 5],
    [5, 2, 6],
    [5, 3, 7],
]

col_masks = [
    [0, 0, 4],
    [0, 1, 5],
    [0, 2, 6],
    [1, 0, 4],
    [1, 1, 5],
    [1, 2, 6],
    [2, 0, 4],
    [2, 1, 5],
    [2, 2, 6],
    [3, 0, 4],
    [3, 1, 5],
    [3, 2, 6],
    [4, 0, 4],
    [4, 1, 5],
    [4, 2, 6],
    [5, 0, 4],
    [5, 1, 5],
    [5, 2, 6],
    [6, 0, 4],
    [6, 1, 5],
    [6, 2, 6],
]


class SimpleFlatUCB1(Player):
    def choose_action(self) -> int:
        self.new_turn()
        return self.calculate_turn()

    def inform(self, column: int, opponent: bool):
        if opponent:
            player = 2
        else:
            player = 1
        update_board(self.board, player, column)

    def reset(self):
        self.board_shape = (6, 7)
        self.board = np.zeros(self.board_shape).astype(int)

    def __init__(self):
        super().__init__()

        # initialize board
        self.reset()

    def new_turn(self):
        # initalize values and counts for actions
        self.action_value_sums = np.zeros(7)
        self.action_counts = np.zeros(7).astype(int)

        # dont consider full columns
        self.action_value_sums[self.board.min(axis=0) > 0] = -np.inf
        self.action_counts[self.board.min(axis=0) > 0] = 9999999999999

    def calculate_turn(self) -> int:

        # action_value_sums = np.array([1, 2, 3, 4, 5, 6, 7], dtype=float)
        # action_counts = np.ones(7).astype(int)

        start_time = datetime.now()

        sim = MCTS_Simulator(init_board=None, init_player=2)
        counter = 0
        while True:
            passed_time = datetime.now() - start_time
            if ((passed_time.seconds * 1000)) + (
                (passed_time.microseconds) / 1000
            ) > 200:
                break

            next_board = self.board.copy()

            # if an action has not been tried try it
            if (self.action_counts == 0).sum() > 0:
                next_move = self.action_counts.argmin()
            else:
                # else calculate the UCB1-value for each column
                # calculate mean values
                mean_values = self.action_value_sums / self.action_counts

                # calculate upper confidence bounds for trees
                uct_values = mean_values + (
                    2
                    * (1 / np.sqrt(2))
                    * np.sqrt(2 * np.log(self.action_counts.sum()) / self.action_counts)
                )

                next_move = uct_values.argmax()

            update_board(next_board, 1, next_move)

            sim.set_init_board(next_board)
            result = sim.play_round_uniform_random()
            self.action_counts[next_move] += 1
            self.action_value_sums[next_move] += result

            counter += 1

        # print(counter)
        # print(profiling)

        return (
            self.action_value_sums.argmax(),
            self.action_value_sums,
            self.action_counts,
        )


def update_board(board: np.ndarray, player: int, column: int):
    next_row = board[:, column].argmin()

    if next_row > 5:
        print(f"Attempt to add a stone for player {player} in full column {column}")

    board[next_row, column] = player


# sim = MCTS_Simulator(init_board=np.zeros((6, 7)).astype(int), init_player=1)

# results = []
# while True:
#     results.append(sim.play_round_uniform_random())
#     print(np.mean(results))

# np.mean([sim.play_round_uniform_random() for _ in range(1)])


# profiling = [0, 0, 0, 0, 0]


class MCTS_Simulator:
    def __init__(self, init_board: np.ndarray, init_player: int):
        super().__init__()

        self.init_board = init_board
        self.init_player = init_player

    def set_init_board(self, init_board: np.ndarray):
        self.init_board = init_board

    def set_init_player(self, init_player: int):
        self.init_player = init_player

    def play_round_uniform_random(self):
        current_board = self.init_board
        current_player = self.init_player

        while True:
            if current_board[5, :].min() > 0:
                # board is full
                return 0.5

            available_moves = np.where(current_board[5, :] == 0)[0]
            next_move = randint(0, len(available_moves) - 1)
            # next_row = current_board[:, next_move].argmin()
            # current_board[next_row, next_move] = current_player
            update_board(current_board, current_player, next_move)

            # print(current_board)

            if is_win_state_alt(current_board):
                if current_player == 1:
                    return 1.0
                else:
                    return 0.0

            if current_player == 1:
                current_player = 2
            else:
                current_player = 1


def is_win_state_alt(board) -> bool:
    # start_time__ = datetime.now()
    board_shape = board.shape
    board_1 = (board % 2).astype(int)
    board_2 = (board / 2).astype(int)
    __board = board_1 - board_2
    # profiling[0] += (datetime.now() - start_time__).microseconds

    # Test rows
    # start_time__ = datetime.now()
    for mask in row_masks:
        value = sum(__board[mask[0]][mask[1] : mask[2]])
        if abs(value) == 4:
            return True
    # profiling[1] += (datetime.now() - start_time__).microseconds

    # Test columns on transpose array
    # start_time__ = datetime.now()
    reversed_board = [list(i) for i in zip(*__board)]
    for mask in col_masks:
        value = sum(reversed_board[mask[0]][mask[1] : mask[2]])
        if abs(value) == 4:
            return True
    # profiling[2] += (datetime.now() - start_time__).microseconds

    # Test diagonal
    # start_time__ = datetime.now()
    for i in range(board_shape[0] - 3):
        for j in range(board_shape[1] - 3):
            value = 0
            for k in range(4):
                # print(f"[{i}, {j}, {k}],")
                value += __board[i + k][j + k]
                if abs(value) == 4:
                    return True
    # profiling[3] += (datetime.now() - start_time__).microseconds

    # start_time__ = datetime.now()
    reversed_board = np.fliplr(__board)
    # Test reverse diagonal
    for i in range(board_shape[0] - 3):
        for j in range(board_shape[1] - 3):
            value = 0
            for k in range(4):
                value += reversed_board[i + k][j + k]
                if abs(value) == 4:
                    return True
    # profiling[4] += (datetime.now() - start_time__).microseconds

    return False


# board = np.array([x for x in range(6 * 7)]).reshape((6, 7))

# ucb = SimpleFlatUCB1()
# ucb.new_turn()
# next_turn, values, counts = ucb.calculate_turn()
# print(next_turn, values, counts)

