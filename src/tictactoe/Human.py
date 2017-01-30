from tictactoe.Util import *


class Human(object):
    def __init__(self, player):
        self.player = player

    @staticmethod
    def action(state):
        print_board(state)
        action = raw_input('Your move? ')
        return int(action.split(',')[0]), int(action.split(',')[1])

    @staticmethod
    def episode_over(winner):
        if winner == DRAW:
            print 'Game over! It was a draw.'
        else:
            print 'Game over! Winner: Player {0}'.format(winner)