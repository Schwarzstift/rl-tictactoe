import multiprocessing

from tictactoe.Util import *


class Trainer(multiprocessing.Process):

    verbose = False

    def __init__(self, player1, player2, num_games, queue):
        super(Trainer, self).__init__()
        self.player1 = player1
        self.player2 = player2
        self.num_games = num_games
        self.queue = queue
        self.win_counter = {}

    def run(self):
        self.win_counter = self.train_agents_against_each_other(self.num_games,self.player1, self.player2, self.verbose)
        self.queue.put(self.win_counter)
        return

    def train_agents_against_each_other(self, num_games, player1, player2, verbose):
        win_counter = {PLAYER_X: [0], PLAYER_O: [0], DRAW: [0]}
        for i in range(num_games):
            winner = self.play(player1, player2)
            player1.episode_over(winner)
            player2.episode_over(winner)

            for state in [PLAYER_X, PLAYER_O, DRAW]:
                value = 0
                if winner == state:
                    value = 1
                win_counter[state].append(win_counter[state][-1] + value)

            if verbose:
                if i % 100 == 0:
                    print("Process: "+ str(round(i/float(num_games)*100))) + "%"
        return win_counter

    def play(self, agent1, agent2):
        current_field_state = empty_state()
        current_player = agent1.player
        game_state = EMPTY
        for i in range(9):
            if current_player == agent1.player:
                agent1.action(current_field_state)
                current_player = agent2.player
            else:
                agent2.action(current_field_state)
                current_player = agent1.player
            game_state = game_over(current_field_state)
            if game_state != EMPTY:
                return game_state
        return game_state