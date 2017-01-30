import random
from copy import deepcopy

from tictactoe.Global import *


class Agent(object):
    def __init__(self, player, verbose=False, loss_val=0, learning=True):
        self.values = {}
        self.player = player
        self.verbose = verbose
        self.loss_val = loss_val
        self.learning = learning
        self.epsilon = 0.1
        self.alpha = 0.99
        self.prev_state = None
        self.prev_score = 0
        self.count = 0
        self.add(empty_state())

    def episode_over(self, winner):
        self.backup(self.winner_val(winner))
        self.prev_state = None
        self.prev_score = 0

    def action(self, current_field_state):
        r = random.random()
        if r < self.epsilon:
            move = self.choose_a_random_move(current_field_state)
            self.log('>>>>>>> Exploratory action: ' + str(move))
        else:
            move = self.greedy(current_field_state)
            self.log('>>>>>>> Best action: ' + str(move))
        current_field_state[move[0]][move[1]] = self.player
        self.prev_state = self.state_tuple(current_field_state)
        self.prev_score = self.lookup(current_field_state)
        current_field_state[move[0]][move[1]] = EMPTY
        return move

    @staticmethod
    def choose_a_random_move(state):
        available = []
        for i in range(3):
            for j in range(3):
                if state[i][j] == EMPTY:
                    available.append((i, j))
        return random.choice(available)

    def greedy(self, state):
        max_val = -50000
        max_move = None
        if self.verbose:
            cells = []
        for i in range(3):
            for j in range(3):
                if state[i][j] == EMPTY:
                    state[i][j] = self.player
                    val = self.lookup(state)
                    state[i][j] = EMPTY
                    if val > max_val:
                        max_val = val
                        max_move = (i, j)
                    if self.verbose:
                        cells.append('{0:.3f}'.format(val).center(6))
                elif self.verbose:
                    cells.append(NAMES[state[i][j]].center(6))
        if self.verbose:
            print BOARD_FORMAT.format(*cells)
        self.backup(max_val)
        return max_move

    def backup(self, next_val):
        if self.prev_state is not None and self.learning:
            self.values[self.prev_state] += self.alpha * (next_val - self.prev_score)

    def lookup(self, state):
        key = self.state_tuple(state)
        if key not in self.values:
            self.add(key)
        return self.values[key]

    def add(self, state):
        winner = game_over(state)
        tup = self.state_tuple(state)
        self.values[tup] = self.winner_val(winner)

    def winner_val(self, winner):
        if winner == self.player:
            return 1
        elif winner == EMPTY:
            return 0.5
        elif winner == DRAW:
            return 0
        else:
            return self.loss_val

    def print_values(self):
        vals = deepcopy(self.values)
        for key in vals:
            state = [list(key[0]), list(key[1]), list(key[2])]
            cells = []
            for i in range(3):
                for j in range(3):
                    if state[i][j] == EMPTY:
                        state[i][j] = self.player
                        cells.append(str(self.lookup(state)).center(3))
                        state[i][j] = EMPTY
                    else:
                        cells.append(NAMES[state[i][j]].center(3))
            print BOARD_FORMAT.format(*cells)

    @staticmethod
    def state_tuple(state):
        return tuple(state[0]), tuple(state[1]), tuple(state[2])

    def log(self, s):
        if self.verbose:
            print s
