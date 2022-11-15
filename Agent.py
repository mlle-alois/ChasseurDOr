import pickle
import Consts
from random import *


class Agent:
    def __init__(self, alpha=0.99, gamma=0.9, exploration=0, cooling_rate=0.1):

        self.__tool = Consts.PICKAXE
        self.__alpha = alpha
        self.__gamma = gamma
        self.__exploration = exploration
        self.__cooling_rate = cooling_rate
        self.__history = []
        self.__score = 0
        self.__life_points = 5

        self.__position = None
        self.__qtable = {}
        self.__current_radar = {}
        self.__treasure_radar = {}

    def reset(self, start_state, treasure_radar, append_score):
        if append_score:
            self.__history.append(self.__score)
        self.__current_radar = start_state
        self.__treasure_radar = treasure_radar
        self.__score = 0
        self.reset_pv()

    def update_position(self, action):
        self.__position = self.current_radar[Consts.RADAR_ACTION_INDEX[action]]

    def is_on_forbidden_state(self, new_position):
        return new_position == Consts.MAP_WALL or new_position == Consts.RIVER

    def is_on_obstacle(self, new_position):
        return self.is_on_rock(new_position) or self.is_on_log(new_position)

    def is_on_bee(self, new_position):
        return new_position == Consts.BEE

    def is_on_rock(self, new_position):
        return new_position == Consts.ROCK

    def is_on_log(self, new_position):
        return new_position == Consts.LOG

    def is_on_treasure(self, new_position):
        return new_position == Consts.TREASURE

    def is_allowed_to_log(self, index):
        return self.__current_radar[index] == Consts.EMPTY or self.__current_radar[index] == Consts.RIVER

    def agent_has_nothing_behind_him(self, index):
        return self.__current_radar[Consts.RADAR_ACTION_INDEX[index]] == Consts.EMPTY

    def has_good_tool(self, new_position):
        return (self.is_on_rock(new_position) and self.__tool == Consts.PICKAXE) or \
               (self.is_on_bee(new_position) and self.__tool == Consts.SWORD)

    def can_interact_with_log(self, action):
        if (action == Consts.ACTION_UP and self.is_allowed_to_log(Consts.INDEX_TOP)) or \
                (action == Consts.ACTION_RIGHT and self.is_allowed_to_log(Consts.INDEX_RIGHT)) or \
                (action == Consts.ACTION_DOWN and self.is_allowed_to_log(Consts.INDEX_DOWN)) or \
                (action == Consts.ACTION_LEFT and self.is_allowed_to_log(Consts.INDEX_LEFT)) or \
                (action == Consts.ACTION_PULL_UP and self.agent_has_nothing_behind_him(Consts.ACTION_UP)) or \
                (action == Consts.ACTION_PULL_RIGHT and self.agent_has_nothing_behind_him(Consts.ACTION_RIGHT)) or \
                (action == Consts.ACTION_PULL_DOWN and self.agent_has_nothing_behind_him(Consts.ACTION_DOWN)) or \
                (action == Consts.ACTION_PULL_LEFT and self.agent_has_nothing_behind_him(Consts.ACTION_LEFT)):
            return True
        else:
            return False

    def step(self, reward, radar, treasure_radar, action):
        actions = self.get_actions_by_radar(radar)

        if action == Consts.SWORD or action == Consts.PICKAXE:
            self.update_tool(action)

        ## action qui vaut le plus de points
        max_q = max(actions.values())
        actions[action] += self.__alpha * (reward + self.__gamma * max_q - actions[action])

        self.__current_radar = radar
        self.__treasure_radar = treasure_radar
        self.__score += reward

    def heat(self):
        self.__exploration = 1

    ## Récupère les actions dans la qtable à partir d'un radar
    def get_actions_by_radar(self, radar):
        for i in self.__qtable:
            if self.__qtable[i][0] == radar:
                return self.__qtable[i][1][self.__tool]

    def add_radar_to_qtable(self, radar):
        for i in self.__qtable:
            if self.__qtable[i][0] == radar:
                return

        qtable_size = len(self.__qtable)
        self.__qtable[qtable_size] = [radar, {}]

        for tool in Consts.SWORD, Consts.PICKAXE:
            self.__qtable[qtable_size][1][tool] = {}
            for action in self.__available_actions(tool):
                self.__qtable[qtable_size][1][tool][action] = 0

    def best_action(self):
        if uniform(0, 1) < self.__exploration:
            self.__exploration *= self.__cooling_rate
            return choice(self.__available_actions(self.__tool))
        else:
            favorites_actions = []
            for index, value in enumerate(self.__treasure_radar):
                if value == "X":
                    favorites_actions = Consts.FAVORITE_ACTIONS_BY_TREASURE_POSITION[index]
            for key, value in self.__qtable.items():
                if value[0] == self.current_radar:
                    actions = value[1][self.__tool]
                    for action in favorites_actions:
                        actions[action] += Consts.FAVORITE_ACTION_BONUS
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

    def update_tool(self, action):
        self.__tool = action

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
    def treasure_radar(self):
        return self.__treasure_radar

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

    def update_radars(self, radar, treasure_radar):
        self.__current_radar = radar
        self.__treasure_radar = treasure_radar

    def __repr__(self):
        return str(self.__qtable)
