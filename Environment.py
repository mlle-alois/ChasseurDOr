import Consts


class Environment:
    def __init__(self, str_map):
        self.__parse(str_map)
        self.__nb_states = len(self.__states)
        self.lifePoints = 5  # TODO déplacer dans l'agent

    def __parse(self, str_map):
        self.__states = {}
        for row, line in enumerate(str_map.strip().splitlines()):
            for col, char in enumerate(line):
                if char == Consts.MAP_START:
                    self.__start = (row, col, Consts.PICKAXE)
                elif char == Consts.TREASURE:
                    self.__treasure = (row, col)

                for tool in Consts.PICKAXE, Consts.SWORD:
                    self.__states[(row, col, tool)] = char

        self.__rows = row + 1
        self.__cols = col + 1

    def is_forbidden_state(self, state):
        return state not in self.__states \
               or self.is_wall(state) or self.is_river(state)

    def is_treasure(self, state):
        return (state[0], state[1]) == self.__treasure

    def is_wall(self, state):
        return self.__states[state] == Consts.MAP_WALL

    def is_river(self, state):
        return self.__states[state] == Consts.RIVER

    def is_start(self, state):
        return self.__states[state] == Consts.MAP_START

    def is_obstacle(self, state):
        return self.__states[state] == Consts.ROCK or self.__states[state] == Consts.LOG

    def is_log(self, state):
        return self.__states[state] == Consts.LOG

    def is_rock(self, state):
        return self.__states[state] == Consts.ROCK

    def is_bee(self, state):
        return self.__states[state] == Consts.BEE

    # TODO déplacer dans Agent
    def is_dead(self):
        return self.lifePoints == 0

    def is_good_tool(self, state, tool):
        return (self.is_rock(state) and tool == Consts.PICKAXE) or \
               (self.is_bee(state) and tool == Consts.SWORD)

    def do(self, state, action):
        move = Consts.ACTION_MOVES[action]
        tool = move[2] if move[2] != 0 else state[2]
        new_state = (state[0] + move[0], state[1] + move[1], tool)
        reward = Consts.REWARD_DEFAULT

        if self.is_forbidden_state(new_state):
            reward = -2 * self.__nb_states
        elif self.is_obstacle(new_state):
            if self.is_good_tool(new_state, tool):
                state = new_state
            else:
                reward = -2
        #TODO problème l'abeille est en mouvement, cette méthode n'est plus valable
        elif self.is_bee(new_state):
            state = new_state
            if not self.is_good_tool(new_state, tool):
                reward = -3 * self.__nb_states
        else:
            state = new_state
            if self.__states[state] == Consts.TREASURE:
                reward = 3 * self.__nb_states

        return reward, state

    def resetPv(self):
        self.lifePoints = 5

    @property
    def start(self):
        return self.__start

    @property
    def treasure(self):
        return self.__treasure

    @property
    def states(self):
        return list(self.__states.keys())

    @property
    def height(self):
        return self.__rows

    @property
    def width(self):
        return self.__cols

    @property
    def pv(self):
        return self.lifePoints
