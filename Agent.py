import pickle
import Consts
from random import *


class Agent:
    def __init__(self, alpha=1, gamma=0.9, exploration=0, cooling_rate=0.1):

        self.__tool = Consts.PICKAXE
        self.__alpha = alpha
        self.__gamma = gamma
        self.__exploration = exploration
        self.__cooling_rate = cooling_rate
        self.__history = []
        self.__score = 0
        self.__life_points = 5

        self.__position = (0, 0) ##TODO
        self.__qtable = {}
        self.__current_radar = {}

    def reset(self, start_state, append_score):
        if append_score:
            self.__history.append(self.__score)
        self.__current_radar = start_state
        self.__score = 0
        self.reset_pv()

    ## state devient un radar ?
    def step(self, reward, radar, action):
        ## action qui vaut le plus de points ?
        max_q = max(self.__qtable[radar].values())
        self.__qtable[self.current_radar][action] += \
            self.__alpha * (reward + self.__gamma * max_q - self.__qtable[self.current_radar][action])

        self.__current_radar = radar
        self.__score += reward

    def heat(self):
        self.__exploration = 1

    ## Complète la q_table au fur et à mesure
    def get_qtable(self, radar):
        return self.__qtable[radar]

    def update_qtable(self, radar):
        print(radar, self.__qtable)
        for i in self.__qtable:
            if self.__qtable[i][0] == radar:
                return

        qtable_size = len(self.__qtable)
        self.__qtable[qtable_size] = [radar, {}]

        for tool in Consts.SWORD, Consts.PICKAXE:
            self.__qtable[qtable_size][1][tool] = {}
            for action in self.__available_actions(tool):
                self.__qtable[qtable_size][1][tool][action] = 0
        print(self.__qtable)


    def best_action(self):
        if uniform(0, 1) < self.__exploration:
            self.__exploration *= self.__cooling_rate
            return choice(Consts.ACTIONS)
        else:
            # print(self.__qtable)
            actions = self.__qtable[self.__current_radar][self.__tool]
            return max(actions, key=actions.get)

    def __available_actions(self, tool):
        actions = [
            Consts.ACTION_UP, Consts.ACTION_DOWN, Consts.ACTION_LEFT, Consts.ACTION_RIGHT,
            Consts.ACTION_PULL_UP, Consts.ACTION_PULL_DOWN, Consts.ACTION_PULL_RIGHT, Consts.ACTION_PULL_LEFT,
        ]
        if tool != Consts.PICKAXE:
            actions.append(Consts.ACTION_PICKAXE)
        elif tool != Consts.SWORD:
            actions.append(Consts.ACTION_SWORD)

        return actions

    def save(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump((self.__qtable, self.__history), file)

    def load(self, filename):
        with open(filename, 'rb') as file:
            self.__qtable, self.__history = pickle.load(file)

    def reset_pv(self):
        self.__life_points = 5

    def is_dead(self):
        return self.__life_points <= 0

    def hurt(self):
        self.__life_points -= 1

    @property
    def score(self):
        return self.__score

    @property
    def current_radar(self):
        return self.__current_radar

    def current_position(self):
        return self.__position

    @property
    def exploration(self):
        return self.__exploration

    @property
    def history(self):
        return self.__history

    @property
    def life_points(self):
        return self.__life_points

    @property
    def tool(self):
        return self.__tool

    def update_radar(self, radar):
        self.__current_radar = radar

    def __repr__(self):
        return str(self.__qtable)
