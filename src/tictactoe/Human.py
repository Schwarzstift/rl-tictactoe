from tictactoe.Util import *


class Human(object):
    def __init__(self, player):
        self.player = player

    def action(self, current_field):
        illegal_move = True
        while illegal_move:
            print_board(current_field)
            action = raw_input('Your move? ')
            move = int(action.split(',')[0]), int(action.split(',')[1])

            if current_field[move[0]][move[1]] == EMPTY:
                current_field[move[0]][move[1]] = self.player
                illegal_move = False
            else:
                print ("Illegal move! try again")

    def episode_over(self,winner):
        if winner == DRAW:
            print 'Game over! It was a draw.'
        elif winner == self.player:
            print 'Game over! YOU WIN!'
        else:
            print 'Game over! YOU LOST!'

