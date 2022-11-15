def is_treasure_above_agent(adventurer, treasure):
    return adventurer.center_y < treasure.center_y and adventurer.center_x == treasure.center_x


def is_treasure_under_agent(adventurer, treasure):
    return adventurer.center_y > treasure.center_y and adventurer.center_x == treasure.center_x


def is_treasure_left_to_agent(adventurer, treasure):
    return adventurer.center_y == treasure.center_y and adventurer.center_x > treasure.center_x


def is_treasure_right_to_agent(adventurer, treasure):
    return adventurer.center_y == treasure.center_y and adventurer.center_x < treasure.center_x


def is_treasure_diagonal_up_left_to_agent(adventurer, treasure):
    return adventurer.center_y < treasure.center_y and adventurer.center_x > treasure.center_x


def is_treasure_diagonal_up_right_to_agent(adventurer, treasure):
    return adventurer.center_y < treasure.center_y and adventurer.center_x < treasure.center_x


def is_treasure_diagonal_down_left_to_agent(adventurer, treasure):
    return adventurer.center_y > treasure.center_y and adventurer.center_x > treasure.center_x


def is_treasure_diagonal_down_right_to_agent(adventurer, treasure):
    return adventurer.center_y > treasure.center_y and adventurer.center_x < treasure.center_x
