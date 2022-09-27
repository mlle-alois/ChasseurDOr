import Consts


class Environment:
    def __init__(self, str_map):
        self.__parse(str_map)
        self.__nb_states = len(self.__states)

    def __parse(self, str_map):
        self.__states = {}
        for row, line in enumerate(str_map.strip().splitlines()):
            for col, char in enumerate(line):
                if char == Consts.MAP_START:
                    self.__start = (row, col, Consts.PICKAXE)
                elif char == Consts.TREASURE:
                    self.__treasure = (row, col, Consts.PICKAXE)
                self.__states[(row, col, Consts.PICKAXE)] = char

        # TODO enlever ????
        self.__rows = row + 1
        self.__cols = col + 1

    def is_forbidden_state(self, state):
        return state not in self.__states \
               or self.is_wall(state) or self.is_river(state)

    def is_wall(self, state):
        return self.__states[state] == Consts.MAP_WALL

    def is_river(self, state):
        return self.__states[state] == Consts.RIVER

    def is_start(self, state):
        return self.__states[state] == Consts.MAP_START

    def is_treasure(self, state):
        return self.__states[state] == Consts.TREASURE

    def is_obstacle(self, state):
        return self.__states[state] == Consts.ROCK or self.__states[state] == Consts.LOG

    def is_log(self, state):
        return self.__states[state] == Consts.LOG

    def is_rock(self, state):
        return self.__states[state] == Consts.ROCK

    def is_good_tool(self, state, tool):
        return (self.is_log(state) and tool == Consts.AXE) or (self.is_rock(state) and tool == Consts.PICKAXE)

    def do(self, state, action):
        print(action)
        move = Consts.ACTION_MOVES[action]
        tool = move[2] if move[2] != 0 else state[2]
        new_state = (state[0] + move[0], state[1] + move[1], tool)
        reward = Consts.REWARD_DEFAULT

        if self.is_forbidden_state(new_state):
            reward = -2 * self.__nb_states
        elif self.is_obstacle(new_state):
            if self.is_good_tool(new_state, tool):
                self.remove_obstacle(new_state)
                state = new_state
            else:
                reward = -2
        # TODO WOLVES, MORT, PV
        else:
            state = new_state
            if self.__states[state] == Consts.TREASURE:
                reward = 3 * self.__nb_states

        return reward, state

    def remove_obstacle(self, state):
        map_list = Consts.MAP.split('\n')
        for i, ligne_string in enumerate(map_list):
            map_list[i] = list(ligne_string)

        map_list[state[0] + 1][state[1]] = ' '

        for i, ligne_string in enumerate(map_list):
            map_list[i] = ''.join(map_list[i])
        Consts.MAP = '\n'.join(map_list)

        
        # TODO supprimer l'obstacle en front

    def print(self, agent):
        # TODO APRES
        res = ''
        for row in range(self.__rows):
            for col in range(self.__cols):
                state = (row, col)
                if state == agent.state:
                    res += 'A'
                else:
                    res += self.__states[state]
            res += '\n'
        print(res)

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