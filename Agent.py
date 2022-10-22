import pickle
import Consts
from random import *


class Agent:
    def __init__(self, alpha=1, gamma=0.9, exploration=0, cooling_rate=0.1):

        self.__alpha = alpha
        self.__gamma = gamma
        self.__exploration = exploration
        self.__cooling_rate = cooling_rate
        self.__history = []
        self.__score = 0
        self.__life_points = 5

        self.__qtable = {}

        self.__current_radar = None

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

    ##TODO passer les radars
    def init_qtable(self, radars):
        for radar in radars:
            self.__qtable[radar] = {}
            for action in Consts.ACTIONS:
                self.__qtable[radar][action] = 0

    def best_action(self):
        if uniform(0, 1) < self.__exploration:
            self.__exploration *= self.__cooling_rate
            return choice(Consts.ACTIONS)
        else:
            actions = self.__qtable[self.__current_radar]
            return max(actions, key=actions.get)

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

    @property
    def exploration(self):
        return self.__exploration

    @property
    def history(self):
        return self.__history

    @property
    def life_points(self):
        return self.__life_points

    def __repr__(self):
        return str(self.__qtable)
