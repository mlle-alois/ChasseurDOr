import itertools

import Consts


class Environment:
    def __init__(self, str_map):
        self.__parse(str_map)
        self.__nb_states = len(self.__map_coordinates)

        radar_sample = [
            [Consts.TREASURE, Consts.MAP_WALL, Consts.RIVER, Consts.ROCK, Consts.LOG, Consts.BEE, Consts.EMPTY]
        ]
        self.__radars = list(itertools.product(*radar_sample, repeat=9))

    def __parse(self, str_map):
        row = 0
        col = 0

        self.__map_coordinates = {}
        for row, line in enumerate(str_map.strip().splitlines()):
            for col, char in enumerate(line):
                if char == Consts.MAP_START:
                    self.__start = (row, col, Consts.PICKAXE)
                elif char == Consts.TREASURE:
                    self.__treasure = (row, col)

                ## TODO enlever l'outil
                for tool in Consts.PICKAXE, Consts.SWORD:
                    self.__map_coordinates[(row, col, tool)] = char

        self.__rows = row + 1
        self.__cols = col + 1

    def is_forbidden_state(self, point):
        return point not in self.__map_coordinates \
               or self.is_wall(point) or self.is_river(point)

    def is_treasure(self, point):
        return (point[0], point[1]) == self.__treasure

    def is_wall(self, point):
        return self.__map_coordinates[point] == Consts.MAP_WALL

    def is_river(self, point):
        return self.__map_coordinates[point] == Consts.RIVER

    def is_start(self, point):
        return self.__map_coordinates[point] == Consts.MAP_START

    def is_obstacle(self, point):
        return self.__map_coordinates[point] == Consts.ROCK or self.__map_coordinates[point] == Consts.LOG

    def is_log(self, point):
        return self.__map_coordinates[point] == Consts.LOG

    def is_rock(self, point):
        return self.__map_coordinates[point] == Consts.ROCK

    def is_bee(self, point):
        return self.__map_coordinates[point] == Consts.BEE

    def is_good_tool(self, point, tool):
        return (self.is_rock(point) and tool == Consts.PICKAXE) or \
               (self.is_bee(point) and tool == Consts.SWORD)

    ## peut-être même pas besoin de l'ancien radar
    # def do(self, state, action, old_radar, new_radar):
    #     move = Consts.ACTION_MOVES[action]
    #     tool = move[2] if move[2] != 0 else state[2]
    #     new_state = (state[0] + move[0], state[1] + move[1], tool)
    #     agent_position = new_state[5]
    #     reward = Consts.REWARD_DEFAULT
    #
    #     if self.is_forbidden_state(agent_position):
    #         reward = -2 * self.__nb_states
    #     elif self.is_obstacle(agent_position):
    #         if self.is_good_tool(agent_position, tool):
    #             state = new_state
    #         else:
    #             reward = -2
    #     elif self.is_bee(agent_position):
    #         state = new_state
    #         if not self.is_good_tool(agent_position, tool):
    #             reward = -3 * self.__nb_states
    #     else:
    #         state = new_state
    #         if self.is_treasure(agent_position):
    #             reward = 3 * self.__nb_states
    #
    #     return reward, state

    @property
    def start(self):
        return self.__start

    @property
    def treasure(self):
        return self.__treasure

    @property
    def map_coordinates(self):
        return list(self.__map_coordinates.keys())

    @property
    def radars(self):
        return self.__radars

    @property
    def height(self):
        return self.__rows

    @property
    def width(self):
        return self.__cols
