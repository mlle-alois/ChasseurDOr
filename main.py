import os

import arcade
import matplotlib
import matplotlib.pyplot as plt

import Consts
from Agent import Agent
from Environment import Environment
from World import World
from views.MenuView import MenuView

matplotlib.use('TkAgg')


def extract_history(history):
    plt.plot(history)
    plt.show()


if __name__ == '__main__':

    world = World(Agent(), Environment(Consts.MAP))

    if os.path.exists(Consts.FILE_AGENT):
        world.agent.load(Consts.FILE_AGENT)

    width = world.environment.width * Consts.SPRITE_SIZE
    height = world.environment.height * Consts.SPRITE_SIZE

    window = arcade.Window(width, height, 'Gold Digger')

    window.show_view(MenuView(world, width, height))
    arcade.run()

    world.agent.save(Consts.FILE_AGENT)

    # print(agent.score)

    # plt.plot(agent.history)
    # plt.show()
