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
ACTION_PUSH = 'Ps'
ACTION_PULL = 'Pl'
ACTION_PICKAXE = 'P'
ACTION_SWORD = 'S'
ACTIONS = [ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT, ACTION_PICKAXE, ACTION_SWORD, ACTION_PULL, ACTION_PUSH]

## TODO ajouter push/pull dans toutes les directions ?
ACTION_MOVES = {
    ACTION_UP: (0, 30),
    ACTION_DOWN: (0, -30),
    ACTION_LEFT: (-30, 0),
    ACTION_RIGHT: (30, 0),
    ## enlever les outils
    ACTION_PICKAXE: (0, 0),
    ACTION_SWORD: (0, 0)
    ## switch_tool ?
}

REWARD_DEFAULT = -1

SPRITE_SIZE = 32

FILE_AGENT = 'agent.golddigger'

BEE_SPEED = 1.0
BEE_INTERVAL = 50

RESTART_AUTOMATICALLY = True
