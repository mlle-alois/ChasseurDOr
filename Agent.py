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

    def reset(self, start_state, append_score):
        if append_score:
            self.__history.append(self.__score)
        self.__state = start_state
        self.__score = 0
        self.resetPv()

    def step(self, reward, state, action):
        maxQ = max(self.__qtable[state].values())
        self.__qtable[self.state][action] += \
            self.__alpha * (reward + self.__gamma * maxQ - self.__qtable[self.state][action])

        self.__state = state
        self.__score += reward

    def heat(self):
        self.__exploration = 1

    def init_qtable(self, states):
        for state in states:
            self.__qtable[state] = {}
            for action in Consts.ACTIONS:
                self.__qtable[state][action] = 0

    def best_action(self):
        if uniform(0, 1) < self.__exploration:
            self.__exploration *= self.__cooling_rate
            return choice(Consts.ACTIONS)
        else:
            actions = self.__qtable[self.__state]
            return max(actions, key=actions.get)

    def save(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump((self.__qtable, self.__history), file)

    def load(self, filename):
        with open(filename, 'rb') as file:
            self.__qtable, self.__history = pickle.load(file)

    def resetPv(self):
        self.__life_points = 5

    def is_dead(self):
        return self.__life_points <= 0

    def hurt(self):
        self.__life_points -= 1

    @property
    def score(self):
        return self.__score

    @property
    def state(self):
        return self.__state

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
