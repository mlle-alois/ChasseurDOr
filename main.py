import os

import arcade
import matplotlib
import matplotlib.pyplot as plt

import Consts
from Agent import Agent
from Environment import Environment
from views.MenuView import MenuView

matplotlib.use('TkAgg')


def extract_history(history):
    plt.plot(history)
    plt.show()


if __name__ == '__main__':
    env = Environment(Consts.MAP)

    agent = Agent(env)
    agent.learn(0)

    if os.path.exists(Consts.FILE_AGENT):
        agent.load(Consts.FILE_AGENT)

    width = agent.environment.width * Consts.SPRITE_SIZE
    height = agent.environment.height * Consts.SPRITE_SIZE

    window = arcade.Window(width, height, 'Gold Digger')

    window.show_view(MenuView(agent, width, height))
    arcade.run()

    agent.save(Consts.FILE_AGENT)

    #print(agent.score)

    #plt.plot(agent.history)
    #plt.show()
