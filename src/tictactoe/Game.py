"""
Reference implementation of the Tic-Tac-Toe value function learning agent described in Chapter 1 of 
"Reinforcement Learning: An Introduction" by Sutton and Barto. The agent contains a lookup table that
maps states to values, where initial values are 1 for a win, 0 for a draw or loss, and 0.5 otherwise.
At every move, the agent chooses either the maximum-value move (greedy) or, with some probability
epsilon, a random move (exploratory); by default epsilon=0.1. The agent updates its value function 
(the lookup table) after every greedy move, following the equation:

    V(s) <- V(s) + alpha * [ V(s') - V(s) ]

This particular implementation addresses the question posed in Exercise 1.1:
    
    What would happen if the RL agent taught itself via self-play?

The result is that the agent learns only how to maximize its own potential payoff, without consideration
for whether it is playing to a win or a draw. Even more to the point, the agent learns a myopic strategy
where it basically has a single path that it wants to take to reach a winning state. If the path is blocked
by the opponent, the values will then usually all become 0.5 and the player is effectively moving randomly.

Created by Wesley Tansey
1/21/2013
Code released under the MIT license.
"""

import csv
import matplotlib.pyplot as plt

from tictactoe.Agent import Agent
from tictactoe.Global import *


def print_board(state):
    cells = []
    # noinspection PyShadowingNames
    for i in range(3):
        for j in range(3):
            cells.append(NAMES[state[i][j]].center(6))
    print BOARD_FORMAT.format(*cells)



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


def play(agent1, agent2):
    current_field_state = empty_state()
    for i in range(9):
        if i % 2 == 0:
            move = agent1.action(current_field_state)
        else:
            move = agent2.action(current_field_state)
        current_field_state[move[0]][move[1]] = (i % 2) + 1
        winner = game_over(current_field_state)
        if winner != EMPTY:
            return winner
    return winner


def measure_performance_vs_random(agent1, agent2):
    epsilon1 = agent1.epsilon
    epsilon2 = agent2.epsilon
    agent1.epsilon = 0
    agent2.epsilon = 0
    agent1.learning = False
    agent2.learning = False
    r1 = Agent(1)
    r2 = Agent(2)
    r1.epsilon = 1
    r2.epsilon = 1
    probs = [0, 0, 0, 0, 0, 0]
    games = 100
    for i in range(games):
        winner = play(agent1, r2)
        if winner == PLAYER_X:
            probs[0] += 1.0 / games
        elif winner == PLAYER_O:
            probs[1] += 1.0 / games
        else:
            probs[2] += 1.0 / games
    for i in range(games):
        winner = play(r1, agent2)
        if winner == PLAYER_O:
            probs[3] += 1.0 / games
        elif winner == PLAYER_X:
            probs[4] += 1.0 / games
        else:
            probs[5] += 1.0 / games
    agent1.epsilon = epsilon1
    agent2.epsilon = epsilon2
    agent1.learning = True
    agent2.learning = True
    return probs


def measure_performance_vs_each_other(agent1, agent2):
    # epsilon1 = agent1.epsilon
    # epsilon2 = agent2.epsilon
    # agent1.epsilon = 0
    # agent2.epsilon = 0
    # agent1.learning = False
    # agent2.learning = False
    probs = [0, 0, 0]
    games = 100
    for i in range(games):
        winner = play(agent1, agent2)
        if winner == PLAYER_X:
            probs[0] += 1.0 / games
        elif winner == PLAYER_O:
            probs[1] += 1.0 / games
        else:
            probs[2] += 1.0 / games
    # agent1.epsilon = epsilon1
    # agent2.epsilon = epsilon2
    # agent1.learning = True
    # agent2.learning = True
    return probs


def draw_result_of_training(perf):
    colors = ['r', 'b', 'g', 'c', 'm', 'b']
    series = ['P1-Win', 'P1-Lose', 'P1-Draw', 'P2-Win', 'P2-Lose', 'P2-Draw']
    for i in range(1, len(perf)):
        plt.plot(perf[0], perf[i], label=series[i - 1], color=colors[i - 1])
    plt.xlabel('Episodes')
    plt.ylabel('Probability')
    plt.title('RL Agent Performance vs. Random Agent\n({0} loss value, self-play)'.format(p1.loss_val))
    # plt.title('P1 Loss={0} vs. P2 Loss={1}'.format(p1.lossval, p2.lossval))
    plt.legend()
    # plt.show()
    # plt.savefig('p1loss{0}vsp2loss{1}.png'.format(p1.lossval, p2.lossval))
    plt.savefig('../../results/selfplay_random_{0}loss.png'.format(p1.loss_val))


def game_loop_computer_vs_human():
    while True:
        p2.verbose = True
        p1 = Human(1)
        winner = play(p1, p2)
        p1.episode_over(winner)
        p2.episode_over(winner)


def train_agents():
    f = open('../../results/results.csv', 'wb')
    writer = csv.writer(f)
    writer.writerow(series)
    perf = [[] for _ in range(len(series) + 1)]
    for i in range(5000):
        if i % 10 == 0:
            print 'Game: {0}'.format(i)
            probs = measure_performance_vs_random(p1, p2)
            writer.writerow(probs)
            f.flush()
            perf[0].append(i)
            for idx, x in enumerate(probs):
                perf[idx + 1].append(x)
        winner = play(p1, p2)
        p1.episode_over(winner)
        p2.episode_over(winner)
    f.close()
    return perf


if __name__ == "__main__":
    p1 = Agent(1, loss_val=-1)
    p2 = Agent(2, loss_val=-1)
    r1 = Agent(1, learning=False)
    r2 = Agent(2, learning=False)
    r1.epsilon = 1
    r2.epsilon = 1
    series = ['P1-Win', 'P1-Lose', 'P1-Draw', 'P2-Win', 'P2-Lose', 'P2-Draw']
    perf = train_agents()
    draw_result_of_training(perf)
    game_loop_computer_vs_human()
