import os
import arcade

import matplotlib
import matplotlib.pyplot as plt

import Consts
from Agent import Agent
from Environment import Environment
from MazeWindow import MazeWindow

matplotlib.use('TkAgg')


def extract_history(history):
    plt.plot(history)
    plt.show()

if __name__ == '__main__':
    env = Environment(Consts.MAZE, False)

    agent = Agent(env)
    if os.path.exists(Consts.FILE_AGENT):
        agent.load(Consts.FILE_AGENT)

    windows = MazeWindow(agent)
    windows.setup()
    arcade.run()

    agent.save(Consts.FILE_AGENT)

    print(agent.score)

    plt.plot(agent.history)
    plt.show()
