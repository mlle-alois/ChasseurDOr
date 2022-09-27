MAP = """
#########################
#.  R           R       #
#     RRRRR     M    RRR#
#        MMM    M       #
#RR     M   M  M  RR    #
#     MM  R  MM   MM    #
#     M         RM      #
# R  M           M    RR#
#         R  RR M    R  #
#   RRRR        M    R $#
#########################
"""

MAP_START = '.'
TREASURE = '$'
MAP_WALL = '#'
RIVER = 'M'
ROCK = 'R'
LOG = 'L'
WOLF = 'W'
SWORD = 'G'
PICKAXE = 'P'
AXE = 'A'

ACTION_UP = 'U'
ACTION_DOWN = 'D'
ACTION_LEFT = 'L'
ACTION_RIGHT = 'R'
ACTION_WAIT = 'W'
ACTION_PICKAXE = 'P'
ACTION_AXE = 'A'
ACTION_SWORD = 'S'
ACTIONS = [ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT, ACTION_WAIT, ACTION_PICKAXE, ACTION_AXE, ACTION_SWORD]

ACTION_MOVES = {
    ACTION_UP: (-1, 0, 0),
    ACTION_DOWN: (1, 0, 0),
    ACTION_LEFT: (0, -1, 0),
    ACTION_RIGHT: (0, 1, 0),
    ACTION_WAIT: (0, 0, 0),
    ACTION_PICKAXE: (0, 0, PICKAXE),
    ACTION_AXE: (0, 0, AXE),
    ACTION_SWORD: (0, 0, SWORD)
}

REWARD_DEFAULT = -1

SPRITE_SIZE = 32

FILE_AGENT = 'agent.golddigger'
