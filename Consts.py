MAP = """
#########################
#.  RLL  B      R       #
#LL   RRRRRLLL  MLLLLRRR#
#L  LL   MMM    M LLLL  #
#RR LLLLM   M  M  RR    #
#     MM  R  MM   MMRRRR#
# L LLM L  B  LLRM    LL#
# R LM    LLLLL  MRRRRRL#
#     LLL R  RR M   LL  #
#   RRRR   LLL  M   LL $#
#########################
"""

MAP_START = '.'
TREASURE = '$'
MAP_WALL = '#'
RIVER = 'M'
AGENT = 'A'
ROCK = 'R'
LOG = 'L'
BEE = 'B'
EMPTY = ' '
SWORD = 'S'
PICKAXE = 'P'

ACTION_UP = 'U'
ACTION_DOWN = 'D'
ACTION_LEFT = 'L'
ACTION_RIGHT = 'R'
ACTION_PULL_UP = 'Pu'
ACTION_PULL_DOWN = 'Pd'
ACTION_PULL_RIGHT = 'Pr'
ACTION_PULL_LEFT = 'Pl'
ACTION_PICKAXE = 'P'
ACTION_SWORD = 'S'
ACTIONS = [
    ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT,
    ACTION_PICKAXE, ACTION_SWORD,
    ACTION_PULL_UP, ACTION_PULL_DOWN, ACTION_PULL_RIGHT, ACTION_PULL_LEFT
]

#TODO il est possible que les données ne soient pas bonnes au niveau des -1 (lecture inversée sur la map)
ACTION_MOVES = {
    ACTION_UP: (-1, 0),
    ACTION_DOWN: (1, 0),
    ACTION_LEFT: (0, -1),
    ACTION_RIGHT: (0, 1),
    ACTION_PULL_UP: (-1, 0),
    ACTION_PULL_DOWN: (1, 0),
    ACTION_PULL_LEFT: (0, -1),
    ACTION_PULL_RIGHT: (0, 1),
    ACTION_PICKAXE: (0, 0),
    ACTION_SWORD: (0, 0)
    ## TODO switch_tool ?
}

RADAR_ACTION_INDEX = {
    ACTION_UP: 2,
    ACTION_DOWN: 8,
    ACTION_LEFT: 4,
    ACTION_RIGHT: 6,
    ACTION_PULL_UP: 2,
    ACTION_PULL_DOWN: 8,
    ACTION_PULL_RIGHT: 4,
    ACTION_PULL_LEFT: 6,
    ACTION_PICKAXE: 5,
    ACTION_SWORD: 5
}

REWARD_DEFAULT = -1

SPRITE_SIZE = 32

FILE_AGENT = 'agent.golddigger'

BEE_SPEED = 1.0
BEE_INTERVAL = 50

RESTART_AUTOMATICALLY = True
