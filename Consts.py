MAZE = """
#.#############
#     $       #
#$$$  $   $   #
#     $  $$$ $#
#             #
#     $  $    #
# $$$$$$$$    #
#     $  $$   #
#        $    #
#             #
#############*#
"""

ACTION_UP = 'U'
ACTION_DOWN = 'D'
ACTION_LEFT = 'L'
ACTION_RIGHT = 'R'
ACTIONS = [ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT]

ACTION_MOVES = {ACTION_UP: (-1, 0),
                ACTION_DOWN: (1, 0),
                ACTION_LEFT: (0, -1),
                ACTION_RIGHT: (0, 1)}

MAZE_START = '.'
EXTERN_MAZE_WALL = '#'
INTERN_MAZE_WALLS = '$'
MAZE_GOAL = '*'

REWARD_DEFAULT = -1

SPRITE_SIZE = 64

FILE_AGENT = 'agent.al2'