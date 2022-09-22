import pickle
import Consts
from random import *

class Agent:
    def __init__(self, env, alpha=1, gamma=1, exploration=0, cooling_rate=0.9999):
        self.__env = env
        self.reset(False)
        self.__init_qtable()
        self.__alpha = alpha
        self.__gamma = gamma
        self.__exploration = exploration
        self.__cooling_rate = cooling_rate
        self.__history = []

    def reset(self, append_score=True):
        if append_score:
            self.__history.append(self.__score)
        self.__state = self.__env.start
        self.__score = 0

    def heat(self):
        self.__exploration = 1

    def __init_qtable(self):
        self.__qtable = {}
        for state in self.__env.states:
            self.__qtable[state] = {}
            for action in Consts.ACTIONS:
                self.__qtable[state][action] = 0

    def step(self):
        action = self.best_action()
        reward, state = self.__env.do(self.state, action)

        maxQ = max(self.__qtable[state].values())
        self.__qtable[self.state][action] += \
            self.__alpha * (reward + self.__gamma * maxQ - self.__qtable[self.state][action])
        self.__state = state
        self.__score += reward
        return action, reward

    def best_action(self):
        if uniform(0, 1) < self.__exploration:
            self.__exploration *= self.__cooling_rate
            return choice(Consts.ACTIONS)
        else:
            actions = self.__qtable[self.__state]
            return max(actions, key=actions.get)

    def learn(self, iterations):
        for i in range(iterations):
            self.reset()
            while self.state != self.__env.goal:
                self.step()

    def save(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump((self.__qtable, self.__history), file)

    def load(self, filename):
        with open(filename, 'rb') as file:
            self.__qtable, self.__history = pickle.load(file)

    @property
    def score(self):
        return self.__score

    @property
    def state(self):
        return self.__state

    @property
    def environment(self):
        return self.__env

    @property
    def exploration(self):
        return self.__exploration

    @property
    def history(self):
        return self.__history

    def __repr__(self):
        return str(self.__qtable)
