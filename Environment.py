import Consts


class Environment:
    def __init__(self, str_maze, brickwalls):
        self.__parse(str_maze)
        self.__nb_states = len(self.__states)
        self.__brickwalls = brickwalls

    def __parse(self, str_maze):
        self.__states = {}
        for row, line in enumerate(str_maze.strip().splitlines()):
            for col, char in enumerate(line):
                if char == Consts.MAZE_START:
                    self.__start = (row, col)
                elif char == Consts.MAZE_GOAL:
                    self.__goal = (row, col)
                self.__states[(row, col)] = char

        self.__rows = row + 1
        self.__cols = col + 1

    def is_forbidden_state(self, state):
        if self.__brickwalls:
            return state not in self.__states \
                   or self.is_extern_wall(state) or self.is_intern_wall(state) or self.is_start(state)
        return state not in self.__states \
               or self.is_extern_wall(state) or self.is_start(state)

    def is_extern_wall(self, state):
        return self.__states[state] == Consts.EXTERN_MAZE_WALL

    def is_intern_wall(self, state):
        return self.__states[state] == Consts.INTERN_MAZE_WALLS

    def is_start(self, state):
        return self.__states[state] == Consts.MAZE_START

    def is_goal(self, state):
        return self.__states[state] == Consts.MAZE_GOAL

    def do(self, state, action):
        move = Consts.ACTION_MOVES[action]
        new_state = (state[0] + move[0], state[1] + move[1])
        reward = Consts.REWARD_DEFAULT

        if self.is_forbidden_state(new_state):
            reward = -2 * self.__nb_states
        elif self.is_intern_wall(new_state):
            state = new_state
            reward = -2 * self.__nb_states
        else:
            state = new_state
            if self.__states[state] == Consts.MAZE_GOAL:
                reward = self.__nb_states

        return reward, state

    def print(self, agent):
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
    def goal(self):
        return self.__goal

    @property
    def states(self):
        return list(self.__states.keys())

    @property
    def height(self):
        return self.__rows

    @property
    def width(self):
        return self.__cols