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
from tictactoe.Human import Human
from tictactoe.Util import *


def play(agent1, agent2):
    current_field_state = empty_state()
    current_player = agent1.player
    for i in range(9):
        if current_player == agent1.player:
            move = agent1.action(current_field_state)
            current_player = agent2.player
        else:
            move = agent2.action(current_field_state)
            current_player = agent1.player
        winner = game_over(current_field_state)
        if winner != EMPTY:
            return winner
    return winner


def draw_results(win_counter):
    fig = plt.figure()
    fig.subplots_adjust(bottom= 0.15)
    ax = fig.add_subplot(111)
    for i in range(0,len(win_counter)):
        ax.plot(range(len(win_counter[i])), win_counter[i], label=series_each_other[i])
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),
              fancybox=True, shadow=True, ncol=5)
    fig.show()


def train_agents_against_each_other():
    win_counter = [[0], [0], [0]]
    games=20000
    for i in range(games):
        if i % 100 == 0:
            print "Game: " + str(i) + " of: " + str(games)

        winner = play(p1, p2)
        p1.episode_over(winner)
        p2.episode_over(winner)

        for i in range(3):
            value = 0
            if winner == i+1:
                value = 1
            win_counter[i].append(win_counter[i][-1]+value)
    draw_results(win_counter)


def game_loop_computer_vs_human():
    while True:
        p2.verbose = True
        p1 = Human(1)
        winner = play(p1, p2)
        p1.episode_over(winner)
        p2.episode_over(winner)

if __name__ == "__main__":
    p1 = Agent(PLAYER_X, loss_val=-1)
    p2 = Agent(PLAYER_O, loss_val=-1)
    series_each_other = ['P1-Win', 'P2-Win', 'Draw']
    train_agents_against_each_other()
    plt.show()
    # game_loop_computer_vs_human()
