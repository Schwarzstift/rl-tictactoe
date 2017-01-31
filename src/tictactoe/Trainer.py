import threading

from tictactoe.Util import PLAYER_O, PLAYER_X, DRAW, play


class Trainer(threading.Thread):
    writeLock = threading.Lock()
    player_o_win = []
    player_x_win = []
    draw = []
    num_trainer = 1
    games = 2000

    def __init__(self, player1, player2):
        threading.Thread.__init__(self)
        Trainer.num_trainer -=1
        self.player1 = player1
        self.player2 = player2
        pass

    def run(self):
        print("Start training...")
        result = self.train_agents_against_each_other()

        Trainer.writeLock.acquire()

        Trainer.player_o_win.append(result[PLAYER_O])
        Trainer.player_x_win.append(result[PLAYER_X])
        Trainer.draw.append(result[DRAW])

        Trainer.writeLock.release()

    def train_agents_against_each_other(self):
        win_counter = {PLAYER_X: [0], PLAYER_O: [0], DRAW: [0]}
        for i in range(Trainer.games):
            winner = play(self.player1, self.player2)
            self.player1.episode_over(winner)
            self.player2.episode_over(winner)

            for state in [PLAYER_X, PLAYER_O, DRAW]:
                value = 0
                if winner == state:
                    value = 1
                win_counter[state].append(win_counter[state][-1] + value)
        return win_counter
