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

import copy
import threading

import matplotlib.pyplot as plt
import pandas as pd

import time

from tictactoe.Agent import Agent
from tictactoe.Human import Human
from tictactoe.Trainer import Trainer
from tictactoe.Util import *
import multiprocessing


def draw_results(win_counter):
    fig = plt.figure()
    fig.subplots_adjust(bottom= 0.15)
    ax = fig.add_subplot(111)
    for i in range(0,len(win_counter)):
        ax.plot(range(len(win_counter[i])), win_counter[i], label=series_each_other[i])
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),
              fancybox=True, shadow=True, ncol=5)
    ax.set_ylabel("Occurred event counter")
    ax.set_xlabel("Total games played")
    ax.set_title("TicTacToe - AI vs. AI")

    fig.show()


def draw_average_results(player_o_wins, player_x_wins, draw):
    results = [player_o_wins, player_x_wins, draw]
    labels = ["Player O Win", "Player X Win", "Draw"]
    plotting_data = pd.DataFrame()
    for result,name in zip(results, labels):
        df = pd.DataFrame(result).transpose()
        df = df.mean(axis=1)
        plotting_data[name] = df

    ax = plotting_data.plot()
    ax.set_title("Average of "+str(len(draw))+" repetitions over "+str(len(draw[0])-1)+ " games")
    ax.set_xlabel("Games played")
    ax.set_ylabel("Counter of occurrence")


def average_training_agents(trainings, agent1, agent2):
    def start_trainer():
        copy_of_agent1 = copy.deepcopy(agent1)
        copy_of_agent2 = copy.deepcopy(agent2)
        t = Trainer(copy_of_agent1, copy_of_agent2)
        t.start()
        return t

    Trainer.num_trainer = trainings
    trainers = []
    while Trainer.num_trainer > 0:
        if multiprocessing.cpu_count()>threading.active_count():
            trainers.append(start_trainer())
            print "Process: " + str(round(((trainings-Trainer.num_trainer)/float(trainings))*100)) + "%"
        else:
            time.sleep(2)

    for trainer in trainers:
        trainer.join()

    draw_average_results(Trainer.player_o_win, Trainer.player_x_win, Trainer.draw)


def game_loop_computer_vs_human(agent1, agent2):
    t = Trainer(agent1, agent2)
    t.start()
    t.join()

    while True:
        agent2.verbose = True
        p1 = Human(PLAYER_X)
        winner = play(p1, agent2)
        p1.episode_over(winner)
        p2.episode_over(winner)

if __name__ == "__main__":
    p1 = Agent(PLAYER_X, loss_val=-1)
    p2 = Agent(PLAYER_O, loss_val=-1)
    series_each_other = ['P1-Win', 'P2-Win', 'Draw']
    #average_training_agents(20, p1, p2)
    #plt.show()
    game_loop_computer_vs_human(p1,p2)
