import Consts


class Environment:
    def __init__(self, str_map):
        self.__parse(str_map)
        self.__nb_states = len(self.__map_coordinates)

    def __parse(self, str_map):
        row = 0
        col = 0

        self.__map_coordinates = {}
        for row, line in enumerate(str_map.strip().splitlines()):
            for col, char in enumerate(line):
                if char == Consts.MAP_START:
                    self.__start = (row, col)
                elif char == Consts.TREASURE:
                    self.__treasure = (row, col)
                self.__map_coordinates[(row, col)] = char

        self.__rows = row + 1
        self.__cols = col + 1

    def is_forbidden_state(self, point):
        return point not in self.__map_coordinates \
               or self.is_wall(point) or self.is_river(point)

    def is_treasure(self, point):
        return (point[0], point[1]) == self.__treasure

    def is_agent_on_treasure(self, radar):
        return radar == Consts.TREASURE

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
    def map_size(self):
        return len(self.__map_coordinates)

    @property
    def height(self):
        return self.__rows

    @property
    def width(self):
        return self.__cols
