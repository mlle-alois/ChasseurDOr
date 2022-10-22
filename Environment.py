import Consts
import itertools

class Environment:
    def __init__(self, str_map):
        self.__parse(str_map)
        self.__nb_states = len(self.__states)

    def __parse(self, str_map):
        row = 0
        col = 0

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

        a = [[Consts.TREASURE, Consts.MAP_WALL, Consts.RIVER, Consts.ROCK, Consts.LOG, Consts.BEE, Consts.EMPTY]]
        self.__radars = list(itertools.product(*a, repeat=9))

    def is_forbidden_state(self, state):
        return self.is_wall(state) or self.is_river(state)

    def is_treasure(self, state):
        return state == Consts.TREASURE

    def is_wall(self, state):
        return state == Consts.MAP_WALL

    def is_river(self, state):
        return state == Consts.RIVER

    def is_start(self, state):
        return state == Consts.MAP_START

    def is_obstacle(self, state):
        return state == Consts.ROCK or state == Consts.LOG

    def is_log(self, state):
        return state == Consts.LOG

    def is_rock(self, state):
        return state == Consts.ROCK

    def is_bee(self, state):
        return state == Consts.BEE

    def is_good_tool(self, state, tool):
        return (state and tool == Consts.PICKAXE) or \
               (state and tool == Consts.SWORD)

    def do(self, state, action):
        ## move doit donner un nouveau radar
        ## comment faire :(
        move = Consts.ACTION_MOVES[action]
        tool = move[2] if move[2] != 0 else state[2]
        new_radar = (state[0] + move[0], state[1] + move[1], tool)
        agent_position = new_radar[5]
        reward = Consts.REWARD_DEFAULT

        if self.is_forbidden_state(agent_position):
            reward = -2 * self.__nb_states
        elif self.is_obstacle(agent_position):
            if self.is_good_tool(agent_position, tool):
                state = new_radar
            else:
                reward = -2
        # TODO problème l'abeille est en mouvement, cette méthode n'est plus valable
        elif self.is_bee(agent_position):
            state = new_radar
            if not self.is_good_tool(agent_position, tool):
                reward = -3 * self.__nb_states
        else:
            state = new_radar
            if self.is_treasure(agent_position):
                reward = 3 * self.__nb_states

        return reward, state

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
    def radars(self):
        return self.__radars

    @property
    def height(self):
        return self.__rows

    @property
    def width(self):
        return self.__cols
